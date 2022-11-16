import asyncio
import json
from contextlib import contextmanager
from datetime import datetime
from enum import Enum, auto
from logging import Logger, getLogger
from pathlib import Path
from typing import AsyncGenerator

from srsran_controller.common.ip import find_interface_of_address
from srsran_controller.common.uhd import query_sensor
from srsran_controller.configuration import config
from srsran_controller.exceptions import ScanInterruptedError
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
from srsran_controller.uu_events.system_information_block_7 import SIB7_NAME
from srsran_controller.uu_events.uu_sniffer import UuSniffer

SIB_NAMES = {
    MIB_NAME: 'mib',
    SIB1_NAME: 1,
    SIB2_NAME: 2,
    SIB3_NAME: 3,
    SIB4_NAME: 4,
    SIB5_NAME: 5,
    SIB6_NAME: 6,
    SIB7_NAME: 7,
}


def sibs_complete(sibs):
    return 1 in sibs and all(sib in sibs for sib in sibs[1]['scheduled_sibs'])


class ScanState(Enum):
    NONE = auto()
    SIGNALS = auto()
    SIBS = auto()
    ERROR = auto()


class Scanner:
    SIBS_SCAN_TIMEOUT = 60
    SCAN_GAIN = 70

    def __init__(self, logger: Logger = getLogger('srsran_controller')):
        self.last_sync_signals_scan = {}
        self.last_cells_scan = {}
        self.logger = logger
        self.scan_state = ScanState.NONE
        self.progress = (100, 100)
        self.scan_progress_callback = lambda scanner: None

    @property
    def is_scanning(self):
        return self.scan_state in (ScanState.SIBS, ScanState.SIGNALS)

    async def scan(self, band: int, device_name: str = 'UHD', device_args: str = ''):
        """
        Scan all cells in a given band.
        :param band: Band to scan.
        :param device_name: RF device type to use.
        :param device_args: Device specific arguments.
        """
        self.logger.info(f'Scanning band {band}, device: {device_name}, args: {device_args}')

        self._handle_scan_progress(0, 0, ScanState.SIGNALS)
        try:
            cells = await self.scan_sync_signal(band, device_name, device_args)
            cells.sort(key=lambda c: c['cell_id'] <= 2)
            for i, cell in enumerate(cells):
                self._handle_scan_progress(i, len(cells), ScanState.SIBS)
                await self.scan_cell(cell, device_args)
            return cells
        except ScanInterruptedError:
            self._handle_scan_progress(100, 100, ScanState.ERROR)
        finally:
            if self.scan_state != ScanState.ERROR:
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

    async def scan_cell(self, cell: dict, device_args: str) -> dict:
        """
        Scan SIBs of a specific cell.
        :param cell: Cell information.
        :param device_args: RF device related arguments.
        :return: Sibs scanned.
        """
        self.logger.info('Scanning cell earfcn {}, cell_id {}, timeout {}, rx gain {}'.format(
            cell['earfcn'], cell['cell_id'], self.SIBS_SCAN_TIMEOUT, self.SCAN_GAIN)
        )
        sibs = {}
        raw_sibs = []
        with self._run_cell_sniffer(cell['earfcn'], cell['cell_id'], device_args):
            sniffer = UuSniffer(find_interface_of_address(SibsScanner.CLIENT_IP), SibsScanner.CLIENT_IP)
            packet_generator = sniffer.start(use_json=True)
            try:
                await asyncio.wait_for(self._sniff_cell_sibs(packet_generator, sibs, raw_sibs), self.SIBS_SCAN_TIMEOUT)
            except asyncio.TimeoutError:
                pass
            finally:
                await packet_generator.aclose()

        if not sibs_complete(sibs):
            self.logger.warning(f'Could not scan all sibs of cell')

        await self._dump_scan(sibs, raw_sibs, cell, device_args)
        self.last_cells_scan[cell['earfcn'], cell['cell_id']] = sibs
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
        scanner = SyncSignalScanner.create(band, device_name, device_args, self.SCAN_GAIN, self._handle_scan_progress)
        scanner.start()
        try:
            return await scanner.get_sync_signals()
        finally:
            scanner.shutdown()

    @contextmanager
    def _run_cell_sniffer(self, earfcn, cell_id, device_args):
        sibs_sniffer = create_sibs_sniffer(earfcn, cell_id, self.SCAN_GAIN, device_args)
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
            if sibs_complete(sibs):
                break

    async def _dump_scan(self, sibs, raw_sibs, cell, device_args):
        """
        Dump a scan result.
        :param sibs: Parsed SIBs
        :param raw_sibs: Raw pcap SIBs.
        :param cell: Signal related information.
        :param device_args: RF device related arguments.
        """
        if not config.scan_results:
            return
        scan_dir = Path(config.scan_results)
        scan_dir.mkdir(parents=True, exist_ok=True)
        name_base = '{}_{}_{}'.format(datetime.now().timestamp(), cell['earfcn'], cell['cell_id'])
        sib_path = scan_dir / (name_base + '.json')
        self.logger.debug(f'Writing scan results to {sib_path.absolute()}')
        with open(scan_dir / (name_base + '.raw.json'), 'w') as fd:
            json.dump(raw_sibs, fd, indent=4)
        with open(sib_path, 'w') as fd:
            sibs['signal'] = cell
            sibs['time'] = datetime.now().timestamp()
            sibs['gps'] = {
                'locked': await query_sensor('/mboards/0/sensors/gps_locked', address=device_args) != 'false',
                'servo': await query_sensor('/mboards/0/sensors/gps_servo', address=device_args),
                'gga': await query_sensor('/mboards/0/sensors/gps_gpgga', address=device_args),
                'rmc': await query_sensor('/mboards/0/sensors/gps_gprmc', address=device_args),
            }
            json.dump(sibs, fd, indent=4)
