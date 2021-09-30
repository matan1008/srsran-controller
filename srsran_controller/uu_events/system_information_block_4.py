from srsran_controller.common.pyshark import items_in_tree
from srsran_controller.uu_events.common import Q_OFFSET_RANGE_ENUM

SIB4_NAME = 'System Information Block 4'


def parse_neighbours(sib4):
    neighbours = []
    for info in items_in_tree(sib4, 'intraFreqNeighCellList', 'IntraFreqNeighCellInfo_element'):
        neighbours.append({
            'physical_cell_id': int(info.physCellId),
            'q_offset_cell': Q_OFFSET_RANGE_ENUM[int(info.q_OffsetCell)],
        })
    return neighbours


def parse_black_cell(sib4):
    black_cells = []
    for id_range in items_in_tree(sib4, 'intraFreqBlackCellList', 'PhysCellIdRange_element'):
        black_cells.append({
            'start': int(id_range.start),
        })
    return black_cells


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib4 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib4_element')
        ][0].sib4_element

        return {
            'event': SIB4_NAME,
            'data': {
                'intra_freq_neigh_cell_list': parse_neighbours(sib4),
                'intra_freq_black_cell_list': parse_black_cell(sib4),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
