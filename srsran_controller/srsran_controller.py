import logging
import pathlib

import srsran_controller.exceptions as exceptions
from srsran_controller.configuration import config
from srsran_controller.configurations_manager import ConfigurationsManager
from srsran_controller.mission.mission import Mission
from srsran_controller.mission_factory.mission import create as create_mission
from srsran_controller.subscribers_manager import SubscribersManager


class SrsranController:

    def __init__(self, configuration_path):
        self.logger = logging.getLogger('srsran_controller')
        self.logger.addHandler(logging.NullHandler())
        config.reload(configuration_path)
        self.configurations = ConfigurationsManager(config.missions_configurations_folder)
        pathlib.Path(config.missions_configurations_folder).mkdir(parents=True, exist_ok=True)
        self.subscribers = SubscribersManager()
        self._current_mission = None

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
        self.logger.debug('Mission launched successfully')
        return self._current_mission

    async def stop_mission(self):
        """
        Stop the running mission.
        """
        self.logger.info('Stopping current mission')
        if self.current_mission is None:
            self.logger.warning('Mission is not running')
            raise exceptions.MissionIsNotRunningError()

        await self.current_mission.stop()
        self._current_mission = None
        self.logger.debug('Mission stopped successfully')
