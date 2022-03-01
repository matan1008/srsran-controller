import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_7 import SIB7_NAME

SIB7_DATA = (
    'd4c3b2a1020004000000000000000000ffff000095000000041f1e62cc5a0c002d0000002d000000beefdead002d00006d61632d6c74650'
    '1010402ffff03000004062907010a000f00010014906ce03b3c3fc01080'
)


def test_parsing_sib7(tmp_path):
    p = tmp_path / 'sib7.pcap'
    p.write_bytes(bytes.fromhex(SIB7_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        sib7 = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert sib7 == {
        'event': SIB7_NAME,
        'data': {
            't_reselection_geran': 1,
            'carrier_freqs': [
                {
                    'starting_arfcn': 871,
                    'cell_reselection_priority': 0,
                    'band_indicator': 'dcs1800',
                    'q_rx_lev_min': -115,
                    'ncc_permitted': 255,
                    'thresh_x_high': 4,
                    'thresh_x_low': 4,
                }
            ]
        },
        'time': datetime.datetime(2022, 3, 1, 15, 26, 28, 809676),
    }
