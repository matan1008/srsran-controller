import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_4 import SIB4_NAME

SIB4_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d37373030204'
    '35055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d67656e6572'
    '69630004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61676564206'
    '17320332e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f000009000100090000000b00'
    '0e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e657269630000000000580000000'
    '60000008c000000000000001749ad163088aee6690000006900000000000000000000000000000008004500005b566b40004011e6247f'
    '0000017f000001163716d70047fe5a6d61632d6c746501010402ffff03000004201007010a000f000100093cb89221245d890312392cb'
    '263a2f245f28872e1bdc3e40c182d505ae0bcc0000000000000008c000000050000006c0000000000000027ce0500491f5e4101001c00'
    '436f756e746572732070726f76696465642062792064756d706361700200080027ce0500e81ebe2f0300080027ce0500741e5e4104000'
    '8001500000000000000050008000000000000000000000000006c000000'
)


def test_parsing_sib4(tmp_path):
    p = tmp_path / 'sib4.pcap'
    p.write_bytes(bytes.fromhex(SIB4_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        sib4 = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert sib4 == {
        'event': SIB4_NAME,
        'data': {
            'intra_freq_black_cell_list': [],
            'intra_freq_neigh_cell_list': [
                {'physical_cell_id': 184, 'q_offset_cell': 3},
                {'physical_cell_id': 272, 'q_offset_cell': 3},
                {'physical_cell_id': 279, 'q_offset_cell': -3},
                {'physical_cell_id': 288, 'q_offset_cell': -3},
                {'physical_cell_id': 291, 'q_offset_cell': 3},
                {'physical_cell_id': 357, 'q_offset_cell': 3},
                {'physical_cell_id': 398, 'q_offset_cell': 2},
                {'physical_cell_id': 484, 'q_offset_cell': 2},
                {'physical_cell_id': 498, 'q_offset_cell': 2},
                {'physical_cell_id': 57, 'q_offset_cell': -1},
                {'physical_cell_id': 111, 'q_offset_cell': -1},
                {'physical_cell_id': 124, 'q_offset_cell': 1},
                {'physical_cell_id': 193, 'q_offset_cell': 1},
                {'physical_cell_id': 362, 'q_offset_cell': 1},
                {'physical_cell_id': 363, 'q_offset_cell': 1},
                {'physical_cell_id': 377, 'q_offset_cell': 1}
            ]
        },
        'time': datetime.datetime(2021, 10, 12, 15, 43, 26, 808631),
        'enb_ip': '127.0.0.1',
    }
