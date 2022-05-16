import asyncio
import logging
import pathlib

import srsran_controller.exceptions as exceptions
from srsran_controller.configuration import config
from srsran_controller.configurations_manager import ConfigurationsManager
from srsran_controller.mission.mission import Mission
from srsran_controller.mission_factory.mission import create as create_mission
from srsran_controller.products import Products
from srsran_controller.scan.scanner import Scanner
from srsran_controller.scripts.executor import ScriptsExecutor
from srsran_controller.scripts.importer import ScriptsImporter
from srsran_controller.scripts.ping import Ping
from srsran_controller.scripts.sms import Sms
from srsran_controller.subject import Subject
from srsran_controller.subscribers_manager import SubscribersManager


class SrsranController:

    def __init__(self, configuration_path):
        self.logger = logging.getLogger('srsran_controller')
        self.logger.addHandler(logging.NullHandler())
        config.reload(configuration_path)
        self.configurations = ConfigurationsManager(config.missions_configurations_folder)
        pathlib.Path(config.missions_configurations_folder).mkdir(parents=True, exist_ok=True)
        pathlib.Path(config.current_configurations_folder).mkdir(parents=True, exist_ok=True)
        self.subscribers = SubscribersManager()
        self.scanner = Scanner()
        self.scripts_executor = ScriptsExecutor()
        self.scripts_importer = ScriptsImporter(config.scripts_folder)
        pathlib.Path(config.scripts_folder).mkdir(parents=True, exist_ok=True)
        self._current_mission = None
        self._scanning_task = None  # type: asyncio.Task | None
        self.products = Products(config.products_folder)
        # Subjects
        self.events_subject = Subject()
        self.scan_progress_subject = Subject()
        self.script_status_subject = Subject()
        self.script_log_subject = Subject()
        self.scanner.scan_progress_callback = self._handle_scan_progress
        self.scripts_executor.script_status_callback = self._handle_script_status
        self.scripts_executor.script_log_callback = self._handle_script_log

    @property
    def current_mission(self) -> Mission:
        return self._current_mission

    def is_mission_up(self) -> bool:
        """
        :return: True if a mission is running, False otherwise.
        """
        return self.current_mission is not None

    async def launch_mission(self, mission_configuration_id: str) -> Mission:
        """
        Launch a mission.
        :param mission_configuration_id: Mission configuration id.
        :return: Launched mission object.
        :raises exceptions.MissionAlreadyRunningError: When trying to launch a mission while another mission is running.
        """
        self.logger.info(f'Launching mission with configuration {mission_configuration_id}')
        if self.is_mission_up():
            self.logger.warning('A mission is already running')
            raise exceptions.MissionAlreadyRunningError()

        self._current_mission = await create_mission(self.configurations.get_mission(mission_configuration_id))
        self._current_mission.uu_packets_callback = self.scripts_executor.handle_new_uu_packet
        self.current_mission.uu_events_callback = self._handle_uu_event
        self.products.set_mission(self.current_mission)
        self.logger.debug('Mission launched successfully')
        return self._current_mission

    async def stop_mission(self):
        """
        Stop the running mission.
        """
        self.logger.info('Stopping current mission')
        self._assert_mission_running()
        await self.scripts_executor.stop_all()
        await self.current_mission.stop()
        self._current_mission = None
        self.logger.debug('Mission stopped successfully')

    async def run_script(self, script, imsi):
        """
        Run a script for a UE.
        :param srsran_controller.scripts.abstract.AbstractScript script: Script to run.
        :param imsi: UE's IMSI.
        """
        self._assert_mission_running()
        await self.scripts_executor.start_script(script, imsi, self.current_mission)

    async def ping(self, imsi: str) -> Ping:
        """
        Ping a UE.
        :param imsi: UE's IMSI.
        :return: Ping object.
        """
        ping = Ping()
        await self.run_script(ping, imsi)
        return ping

    async def sms(self, imsi: str, text: str, rp_oa: str, tp_oa: str) -> Sms:
        """
        Send SMS to a UE.
        :param imsi: UE's IMSI.
        :param text: Message to send.
        :param rp_oa: RP Originator.
        :param tp_oa: TP Originator.
        :return: SMS script object.
        """
        sms = Sms(text, rp_oa, tp_oa)
        await self.run_script(sms, imsi)
        return sms

    async def scan(self, band: int, device_name: str = 'UHD', device_args: str = ''):
        """
        Start scanning all cells in a given band.
        :param band: Band to scan.
        :param device_name: RF device type to use.
        :param device_args: Device specific arguments.
        """
        if self.scanner.is_scanning:
            self.logger.warning('A scan is already running')
            raise exceptions.ScanAlreadyRunningError()
        self._scanning_task = asyncio.create_task(self.scanner.scan(band, device_name, device_args))

    async def stop_scanning(self):
        self.logger.info('Stopping current scan')
        if self._scanning_task is None or not self.scanner.is_scanning:
            self.logger.warning('Scan is not running')
            raise exceptions.ScanIsNotRunningError()
        self._scanning_task.cancel()
        try:
            await self._scanning_task
        except asyncio.CancelledError:
            pass
        self.logger.debug('Scan stopped successfully')

    def _assert_mission_running(self):
        if self.current_mission is None:
            self.logger.warning('Mission is not running')
            raise exceptions.MissionIsNotRunningError()

    def _handle_uu_event(self, event):
        if event.get('imsi', ''):
            subscriber = self.subscribers.get_by_imsi(event['imsi'])
            if subscriber is not None:
                event['name'] = subscriber.name
        self.products.write_event(event)
        self.events_subject.notify(event)

    def _handle_scan_progress(self, scanner):
        self.scan_progress_subject.notify(scanner)

    def _handle_script_status(self, script):
        self.script_status_subject.notify(script)

    def _handle_script_log(self, script, time, log):
        self.script_log_subject.notify((script, time, log))
