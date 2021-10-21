import asyncio
from contextlib import contextmanager
from logging import Logger, getLogger
from typing import AsyncGenerator

from srsran_controller.common.ip import find_interface_of_address
from srsran_controller.scan.sibs_sniffer import create_sibs_sniffer, SibsScanner
from srsran_controller.scan.sync_signal_scanner import SyncSignalScanner
from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.master_information_block import MIB_NAME
from srsran_controller.uu_events.system_information_block_1 import SIB1_NAME
from srsran_controller.uu_events.system_information_block_2 import SIB2_NAME
from srsran_controller.uu_events.system_information_block_3 import SIB3_NAME
from srsran_controller.uu_events.system_information_block_4 import SIB4_NAME
from srsran_controller.uu_events.system_information_block_5 import SIB5_NAME
from srsran_controller.uu_events.system_information_block_6 import SIB6_NAME
from srsran_controller.uu_events.uu_sniffer import UuSniffer

SIB_NAMES = {
    MIB_NAME: 'mib',
    SIB1_NAME: 1,
    SIB2_NAME: 2,
    SIB3_NAME: 3,
    SIB4_NAME: 4,
    SIB5_NAME: 5,
    SIB6_NAME: 6,
}


class Scanner:
    SIBS_SCAN_TIMEOUT = 60

    def __init__(self, logger: Logger = getLogger('srsran_controller')):
        self.last_sync_signals_scan = {}
        self.last_cells_scan = {}
        self.logger = logger

    async def scan_sync_signal(self, band: int, device_name: str, device_args: str) -> list:
        """
        Scan for synchronization signals.
        :param band: Band to scan cells in.
        :param device_name: RF device to use for scanning, e.g. "UHD".
        :param device_args: RF device related arguments.
        :return: List of found signals and related data - EARFCN, frequency, physical cell id, power.
        """
        self.logger.info('Scanning for sync signals')
        cells = await self._get_sync_signal_scan(band, device_name, device_args)
        self.last_sync_signals_scan[band] = cells
        self.logger.info(f'Found {len(cells)} sync signals')
        return cells

    async def scan_cell(self, earfcn: int, cell_id: int) -> dict:
        """
        Scan SIBs of a specific cell.
        :param earfcn: EARFCN of cell to scan.
        :param cell_id: Physical cell id of cell to scan.
        :return: Sibs scanned.
        """
        self.logger.info(f'Scanning cell earfcn {earfcn}, cell_id {cell_id}')
        sibs = {}
        with self._run_cell_sniffer(earfcn, cell_id):
            sniffer = UuSniffer(find_interface_of_address(SibsScanner.CLIENT_IP), SibsScanner.CLIENT_IP)
            packet_generator = sniffer.start(use_json=True)
            try:
                await asyncio.wait_for(self._sniff_cell_sibs(packet_generator, sibs), self.SIBS_SCAN_TIMEOUT)
            except asyncio.TimeoutError:
                self.logger.warning(f'Could not scan all sibs of cell')
            finally:
                await packet_generator.aclose()

        self.last_cells_scan[earfcn, cell_id] = sibs
        return sibs

    async def _get_sync_signal_scan(self, band: int, device_name: str, device_args: str) -> list:
        """
        Scan for sync signals.
        :param band: Band to scan cells in.
        :param device_name: RF device to use for scanning, e.g. "UHD".
        :param device_args: RF device related arguments.
        :return: List of found signals and related data - EARFCN, frequency, physical cell id, power.
        """
        scanner = SyncSignalScanner.create(band, device_name, device_args)
        scanner.start()
        try:
            return await scanner.get_sync_signals()
        finally:
            scanner.shutdown()

    @contextmanager
    def _run_cell_sniffer(self, earfcn, cell_id):
        sibs_sniffer = create_sibs_sniffer(earfcn, cell_id)
        try:
            yield
        finally:
            sibs_sniffer.shutdown()

    async def _sniff_cell_sibs(self, packet_generator: AsyncGenerator, sibs: dict):
        events_factory = EventsFactory()
        async for packet in packet_generator:
            for event in events_factory.from_packet(packet):
                if event['event'] not in SIB_NAMES:
                    continue
                sibs[SIB_NAMES[event['event']]] = event['data']
            if 1 in sibs and all(sib in sibs for sib in sibs[1]['scheduled_sibs']):
                break
