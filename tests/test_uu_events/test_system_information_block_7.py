import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_7 import SIB7_NAME

SIB7_DATA = (
    '0a0d0d0adc0000004d3c2b1a01000000ffffffffffffffff02003b00313174682047656e20496e74656c28522920436f726528544d292069'
    '372d3131373030204020322e353047487a20287769746820535345342e322900030017004c696e757820352e31352e302d35362d67656e65'
    '7269630004005b0044756d70636170202857697265736861726b2920332e362e3720284769742076332e362e37207061636b616765642061'
    '7320332e362e372d317e7562756e747532322e30342e302b77697265736861726b646576737461626c65290000000000dc00000001000000'
    '580000000100000000000400020002006c6f000009000100090000000b000e000075647020706f7274203538343700000c0017004c696e75'
    '7820352e31352e302d35362d67656e65726963000000000058000000060000007000000000000000e46f3217ab57dbfa4f0000004f000000'
    '000000000000000000000000080045000041e126400040115b837f0000017f000001163716d7002dfe406d61632d6c746501010402ffff03'
    '0000040c2907010a000f00010014906ce03b3c3fc010800070000000050000006c000000000000003df00500335c196b01001c00436f756e'
    '746572732070726f76696465642062792064756d70636170020008003df005002cbda737030008003df00500145c196b040008006b000000'
    '00000000050008000000000000000000000000006c000000'
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
        'time': datetime.datetime(2022, 12, 20, 9, 30, 40, 959781),
        'enb_ip': '127.0.0.1',
    }
