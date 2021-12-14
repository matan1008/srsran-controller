import asyncio
import json
from contextlib import contextmanager
from datetime import datetime
from enum import Enum, auto
from logging import Logger, getLogger
from pathlib import Path
from typing import AsyncGenerator

from srsran_controller.common.ip import find_interface_of_address
from srsran_controller.configuration import config
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


class ScanState(Enum):
    NONE = auto()
    SIGNALS = auto()
    SIBS = auto()


class Scanner:
    SIBS_SCAN_TIMEOUT = 60

    def __init__(self, logger: Logger = getLogger('srsran_controller')):
        self.last_sync_signals_scan = {}
        self.last_cells_scan = {}
        self.logger = logger
        self.scan_state = ScanState.NONE
        self.progress = (100, 100)
        self.scan_progress_callback = lambda scanner: None

    @property
    def is_scanning(self):
        return self.scan_state != ScanState.NONE

    async def scan(self, band: int, device_name: str = 'UHD', device_args: str = ''):
        """
        Scan all cells in a given band.
        :param band: Band to scan.
        :param device_name: RF device type to use.
        :param device_args: Device specific arguments.
        """
        self.logger.info(f'Scanning band {band}')

        self._handle_scan_progress(0, 0, ScanState.SIGNALS)
        try:
            cells = await self.scan_sync_signal(band, device_name, device_args)
            for i, cell in enumerate(cells):
                self._handle_scan_progress(i, len(cells), ScanState.SIBS)
                await self.scan_cell(cell['earfcn'], cell['cell_id'])
            return cells
        finally:
            self._handle_scan_progress(100, 100, ScanState.NONE)

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
        raw_sibs = []
        with self._run_cell_sniffer(earfcn, cell_id):
            sniffer = UuSniffer(find_interface_of_address(SibsScanner.CLIENT_IP), SibsScanner.CLIENT_IP)
            packet_generator = sniffer.start(use_json=True)
            try:
                await asyncio.wait_for(self._sniff_cell_sibs(packet_generator, sibs, raw_sibs), self.SIBS_SCAN_TIMEOUT)
            except asyncio.TimeoutError:
                self.logger.warning(f'Could not scan all sibs of cell')
            finally:
                await packet_generator.aclose()

        self._dump_scan(sibs, raw_sibs, earfcn, cell_id)
        self.last_cells_scan[earfcn, cell_id] = sibs
        return sibs

    def _handle_scan_progress(self, scanned, total, state=None):
        if state is not None:
            self.scan_state = state
        self.progress = (scanned, total)
        self.scan_progress_callback(self)

    async def _get_sync_signal_scan(self, band: int, device_name: str, device_args: str) -> list:
        """
        Scan for sync signals.
        :param band: Band to scan cells in.
        :param device_name: RF device to use for scanning, e.g. "UHD".
        :param device_args: RF device related arguments.
        :return: List of found signals and related data - EARFCN, frequency, physical cell id, power.
        """
        scanner = SyncSignalScanner.create(band, device_name, device_args, self._handle_scan_progress)
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

    async def _sniff_cell_sibs(self, packet_generator: AsyncGenerator, sibs: dict, raw_packets: list):
        events_factory = EventsFactory()
        async for packet in packet_generator:
            if 'mac-lte' in packet:
                raw_packets.append(packet['mac-lte']._all_fields)
            for event in events_factory.from_packet(packet):
                if event['event'] not in SIB_NAMES:
                    continue
                sibs[SIB_NAMES[event['event']]] = event['data']
            if 1 in sibs and all(sib in sibs for sib in sibs[1]['scheduled_sibs']):
                break

    def _dump_scan(self, sibs, raw_sibs, earfcn, cell_id):
        if not config.scan_results:
            return
        scan_dir = Path(config.scan_results)
        scan_dir.mkdir(parents=True, exist_ok=True)
        name_base = f'{datetime.now().timestamp()}_{earfcn}_{cell_id}'
        sib_path = scan_dir / (name_base + '.json')
        self.logger.debug(f'Writing scan results to {sib_path.absolute()}')
        with open(scan_dir / (name_base + '.raw.json'), 'w') as fd:
            json.dump(raw_sibs, fd, indent=4)
        with open(sib_path, 'w') as fd:
            json.dump(sibs, fd, indent=4)
