from srsran_controller.common.pyshark import rrc_get
from srsran_controller.uu_events.common import Q_OFFSET_RANGE_ENUM

SIB4_NAME = 'System Information Block 4'


def parse_neighbours(lte_rrc):
    neighbours = []
    for i in range(int(rrc_get(lte_rrc, 'intraFreqNeighCellList'))):
        neighbours.append({
            'physical_cell_id': int(rrc_get(lte_rrc, 'physCellId')[i]),
            'q_offset_cell': Q_OFFSET_RANGE_ENUM[int(rrc_get(lte_rrc, 'q_OffsetCell')[i])],
        })
    return neighbours


def parse_black_cell(lte_rrc):
    try:
        return [int(start) for start in rrc_get(lte_rrc, 'start')]
    except KeyError:
        return []


def create(pkt):
    try:
        lte_rrc = pkt['mac-lte'].lte_rrc
        if 'lte_rrc_lte-rrc_sib4_element' not in lte_rrc:
            return

        return {
            'event': SIB4_NAME,
            'data': {
                'intra_freq_neigh_cell_list': parse_neighbours(lte_rrc),
                'intra_freq_black_cell_list': parse_black_cell(lte_rrc),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
