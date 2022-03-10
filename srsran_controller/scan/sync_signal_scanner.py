import asyncio
import re
from contextlib import suppress

import docker
from docker.errors import APIError

from srsran_controller.common.docker.entity import Entity
from srsran_controller.configuration import config
from srsran_controller.exceptions import ScanInterruptedError

LOGS_FOOTER_FORMAT = r'Found \d* cells(.*)Bye'
LOGS_FOUND_CELL_FORMAT = (
    r'Found CELL '
    r'(?P<freq>[\d\.]*) MHz, '
    r'EARFCN=(?P<earfcn>\d*), '
    r'PHYID=(?P<cell_id>\d*), '
    r'(?P<prb>\d*) PRB, '
    r'(?P<ports>\d*) ports, '
    r'PSS power=(?P<power>[\d\.\-]*) dBm'
)
LOGS_CURRENT_PROGRESS_FORMAT = r'\[([ \d]*)\/([ \d]*)]'


class SyncSignalScanner(Entity):
    CONTAINER_NAME = 'sync-signal-scanner'
    LOGS_SUFFIX = 'Bye'
    COMMAND = './lib/examples/cell_search -b {} -d {} -a {} -g {}'

    def __init__(self, container, progress_callback):
        super().__init__(container)
        self._progress_callback = progress_callback

    @staticmethod
    def create(band: int, device_name: str, device_args: str, rx_gain: int, progress_callback):
        """
        Create a SyncSignalScanner instance.
        :param band: Band to scan cells in.
        :param device_name: RF device to use for scanning, e.g. "UHD".
        :param device_args: RF device related arguments.
        :param rx_gain: RX gain.
        :param progress_callback: Callback function to be called on progress changes.
        :return: SyncSignalScanner object.
        :rtype: SyncSignalScanner
        """
        client = docker.from_env()
        # Do not auto_remove since we need the logs only after the process ends.
        container = client.containers.create(
            config.scanner_docker_image, SyncSignalScanner.COMMAND.format(band, device_name, device_args, rx_gain),
            auto_remove=False, name=SyncSignalScanner.CONTAINER_NAME, network_mode='none', privileged=True
        )
        return SyncSignalScanner(container, progress_callback)

    async def get_sync_signals(self) -> list:
        """
        Get sync signals.
        :return: List of found signals and related data - EARFCN, frequency, physical cell id, power.
        """
        logs = await self._get_all_logs()
        return self._parse_sync_signals(logs)

    def shutdown(self):
        # Suppress in case it is already killed.
        with suppress(APIError):
            self._container.kill()
        # Suppress in case it is already removed.
        with suppress(APIError):
            self._container.remove()

    def _get_current_logs(self) -> str:
        """
        Read the logs printed until now.
        :return: stdout of sync signals scan.
        """
        return self._container.logs().decode()

    def get_progress(self) -> tuple[int, int]:
        """
        Search for the last progress indication in the logs.
        :return: current EARFCN and total number of EARFCNs.
        """
        try:
            progress = re.findall(LOGS_CURRENT_PROGRESS_FORMAT, self._get_current_logs())[-1]
            return int(progress[0]), int(progress[1])
        except IndexError:
            return 0, 0

    async def _get_all_logs(self) -> str:
        """
        Read all scan logs.
        :return: stdout of sync signals scan.
        """
        previous_scanned = 0
        while not self._get_current_logs().strip().endswith(self.LOGS_SUFFIX):
            scanned, total = self.get_progress()
            if previous_scanned == scanned:
                self._container.reload()
                if self._container.status == 'exited':
                    self.logger.error(f'Sync signals scan interrupted: {self._container.logs().decode()}')
                    raise ScanInterruptedError()
            previous_scanned = scanned
            if total:
                self._progress_callback(scanned, total)
            await asyncio.sleep(1)

        return self._get_current_logs()

    def _parse_sync_signals(self, logs) -> list:
        found_buffer = re.findall(LOGS_FOOTER_FORMAT, logs, re.DOTALL)[0]
        cells = []
        for match in re.finditer(LOGS_FOUND_CELL_FORMAT, found_buffer):
            cell_data = match.groupdict()
            earfcn = int(cell_data['earfcn'])
            cell_id = int(cell_data['cell_id'])
            power = float(cell_data['power'])
            cells.append({
                'freq': float(cell_data['freq']),
                'prb': int(cell_data['prb']),
                'ports': int(cell_data['ports']),
                'earfcn': earfcn, 'cell_id': cell_id, 'power': power,
            })
            self.logger.debug(f'Found sync signals of cell: EARFCN {earfcn}, Cell ID {cell_id}, Power {power}dBm')
        return cells
