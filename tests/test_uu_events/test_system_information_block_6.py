import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_6 import SIB6_NAME

SIB6_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d3737303020'
    '435055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d67656e65'
    '7269630004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61676564'
    '20617320332e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f00000900010009000000'
    '0b000e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e6572696300000000005800'
    '0000060000007c000000000000001849ad16181676805a0000005a00000000000000000000000000000008004500004c588140004011'
    'e41d7f0000017f000001163716d70038fe4b6d61632d6c746501010402ffff03000004303007010a000f00010011092f99086153334d'
    'fa10c2a6669a6421854cc80000007c000000050000006c0000000000000027ce0500491f5e4101001c00436f756e746572732070726f'
    '76696465642062792064756d706361700200080027ce0500e81ebe2f0300080027ce0500741e5e410400080015000000000000000500'
    '08000000000000000000000000006c000000'
)


def test_parsing_sib6(tmp_path):
    p = tmp_path / 'sib6.pcap'
    p.write_bytes(bytes.fromhex(SIB6_DATA))
    with FileCapture(str(p), use_ek=True) as pcap:
        sib6 = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert sib6 == {
        'event': SIB6_NAME,
        'data': {
            't_reselection_utra': 2,
            'utra_fdd_carriers': [
                {
                    'carrier_freq': 3046,
                    'cell_reselection_priority': 2,
                    'p_max_utra': 33,
                    'q_qual_min': -18,
                    'q_rx_lev_min': -115,
                    'thresh_x_high': 4,
                    'thresh_x_low': 6
                },
                {
                    'carrier_freq': 10687,
                    'cell_reselection_priority': 2,
                    'p_max_utra': 33,
                    'q_qual_min': -18,
                    'q_rx_lev_min': -115,
                    'thresh_x_high': 4,
                    'thresh_x_low': 6
                },
                {
                    'carrier_freq': 10662,
                    'cell_reselection_priority': 2,
                    'p_max_utra': 33,
                    'q_qual_min': -18,
                    'q_rx_lev_min': -115,
                    'thresh_x_high': 4,
                    'thresh_x_low': 6
                }
            ]
        },
        'time': datetime.datetime(2021, 10, 12, 15, 43, 29, 388623),
    }
