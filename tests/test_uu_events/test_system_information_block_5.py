import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.system_information_block_5 import SIB5_NAME

SIB5_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d37373030'
    '20435055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d6765'
    '6e657269630004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61'
    '67656420617320332e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f000009000100'
    '090000000b000e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e657269630000'
    '000000580000000600000084000000000000001849ad16507f91336400000064000000000000000000000000000000080045000056'
    '578a40004011e50a7f0000017f000001163716d70042fe556d61632d6c746501010402ffff03000004282007010a000f0001000cc4'
    '123b9284241082413250848210044c5288834282fa8a441078284d000084000000050000006c0000000000000027ce0500491f5e41'
    '01001c00436f756e746572732070726f76696465642062792064756d706361700200080027ce0500e81ebe2f0300080027ce050074'
    '1e5e41040008001500000000000000050008000000000000000000000000006c000000'
)


def test_parsing_sib5(tmp_path):
    p = tmp_path / 'sib5.pcap'
    p.write_bytes(bytes.fromhex(SIB5_DATA))
    with FileCapture(str(p), use_ek=True) as pcap:
        sib5 = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert sib5 == {
        'event': SIB5_NAME,
        'data': {
            'inter_freq_carriers': [
                {
                    'allowed_meas_bandwidth': 25,
                    'cell_reselection_priority': 0,
                    'dl_carrier_freq': 9335,
                    'inter_freq_neigh_cell_list': [],
                    'neigh_cell_config': 'The MBSFN subframe '
                                         'allocations of all '
                                         'neighbour cells are '
                                         'identical to or '
                                         'subsets of that in '
                                         'the serving cell',
                    'presence_antenna_port1': False,
                    'q_rx_lev_min': -122,
                    't_reselection_eutra': 2,
                    'thresh_x_high': 4,
                    'thresh_x_low': 4
                },
                {
                    'allowed_meas_bandwidth': 25,
                    'cell_reselection_priority': 0,
                    'dl_carrier_freq': 9235,
                    'inter_freq_neigh_cell_list': [],
                    'neigh_cell_config': 'The MBSFN subframe '
                                         'allocations of all '
                                         'neighbour cells are '
                                         'identical to or '
                                         'subsets of that in '
                                         'the serving cell',
                    'presence_antenna_port1': False,
                    'q_rx_lev_min': -122,
                    't_reselection_eutra': 2,
                    'thresh_x_high': 4,
                    'thresh_x_low': 4
                },
                {
                    'allowed_meas_bandwidth': 6,
                    'cell_reselection_priority': 6,
                    'dl_carrier_freq': 550,
                    'inter_freq_neigh_cell_list': [],
                    'neigh_cell_config': 'The MBSFN subframe '
                                         'allocations of all '
                                         'neighbour cells are '
                                         'identical to or '
                                         'subsets of that in '
                                         'the serving cell',
                    'presence_antenna_port1': False,
                    'q_rx_lev_min': -120,
                    't_reselection_eutra': 2,
                    'thresh_x_high': 34,
                    'thresh_x_low': 4
                },
                {
                    'allowed_meas_bandwidth': 6,
                    'cell_reselection_priority': 7,
                    'dl_carrier_freq': 3050,
                    'inter_freq_neigh_cell_list': [{'physical_cell_id': 322, 'q_offset_cell': -2}],
                    'neigh_cell_config': 'The MBSFN subframe '
                                         'allocations of all '
                                         'neighbour cells are '
                                         'identical to or '
                                         'subsets of that in '
                                         'the serving cell',
                    'presence_antenna_port1': False,
                    'q_rx_lev_min': -120,
                    't_reselection_eutra': 2,
                    'thresh_x_high': 8,
                    'thresh_x_low': 4
                }
            ]
        },
        'time': datetime.datetime(2021, 10, 12, 15, 43, 28, 98574),
    }
