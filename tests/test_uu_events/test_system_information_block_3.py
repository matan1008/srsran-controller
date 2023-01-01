import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_3 import SIB3_NAME

SIB23_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d3737303020435'
    '055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d67656e65726963'
    '0004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61676564206173203'
    '32e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f000009000100090000000b000e000075'
    '647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e6572696300000000005800000006000000940'
    '00000000000001749ad16e4bc03d37300000073000000000000000000000000000000080045000065563e40004011e6477f0000017f0000'
    '01163716d70051fe646d61632d6c746501010402ffff030000041e0007010a000f000100824c95bf64ae34d8125800600020011068bf52a'
    'bc1a800ca00c02bdc801c584000c0044945189f848000000000000094000000050000006c0000000000000027ce0500491f5e4101001c00'
    '436f756e746572732070726f76696465642062792064756d706361700200080027ce0500e81ebe2f0300080027ce0500741e5e410400080'
    '01500000000000000050008000000000000000000000000006c000000'
)


def test_parsing_sib3(tmp_path):
    p = tmp_path / 'sib3.pcap'
    p.write_bytes(bytes.fromhex(SIB23_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        sib3 = list(EventsFactory().from_packet(list(pcap)[0]))[1]
    assert sib3 == {
        'event': SIB3_NAME,
        'data': {
            'allowed_meas_bandwidth': 6,
            'cell_reselection_priority': 4,
            'neigh_cell_config': 'The MBSFN subframe allocations of all '
                                 'neighbour cells are identical to or subsets of '
                                 'that in the serving cell',
            'presence_antenna_port1': False,
            'q_hyst': 4,
            'q_rx_lev_min': -122,
            's_intra_search': 62,
            's_non_intra_search': 10,
            't_reselection_eutra': 2,
            'thresh_serving_low': 4
        },
        'time': datetime.datetime(2021, 10, 12, 15, 43, 26, 478671),
        'enb_ip': '127.0.0.1',
    }
