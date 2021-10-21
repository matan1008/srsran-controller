import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_1 import SIB1_NAME

SIB1_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d37373030204'
    '35055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d67656e6572'
    '69630004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61676564206'
    '17320332e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f000009000100090000000b00'
    '0e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e657269630000000000580000000'
    '600000080000000000000001749ad16d37e58cd6000000060000000000000000000000000000000080045000052563240004011e6667f'
    '0000017f000001163716d7003efe516d61632d6c746501010402ffff030000041d6507010a000f000140d09403a1281e97a604b140304'
    '8430103085844c23790000000000080000000050000006c0000000000000027ce0500491f5e4101001c00436f756e746572732070726f'
    '76696465642062792064756d706361700200080027ce0500e81ebe2f0300080027ce0500741e5e4104000800150000000000000005000'
    '8000000000000000000000000006c000000'
)


def test_parsing_sib1(tmp_path):
    p = tmp_path / 'sib1.pcap'
    p.write_bytes(bytes.fromhex(SIB1_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        sib1 = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert sib1 == {
        'event': SIB1_NAME,
        'data': {
            'band': 3,
            'cell_barred': False,
            'cell_identity': 39362576,
            'csg_indication': False,
            'intra_freq_reselection': True,
            'plmns': [{'plmn': '42501', 'reserved': False},
                      {'plmn': '42507', 'reserved': False}],
            'q_rxlevmin': -122,
            'scheduled_sibs': [3, 4, 5, 6],
            'tac': 19411
        },
        'time': datetime.datetime(2021, 10, 12, 15, 43, 26, 383563),
    }
