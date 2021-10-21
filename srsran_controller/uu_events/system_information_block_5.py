from srsran_controller.common.pyshark import items_in_tree
from srsran_controller.uu_events.common import NEIGH_CELL_CONFIG_DESC, ALLOWED_MEAS_BANDWIDTH_ENUM, Q_OFFSET_RANGE_ENUM

SIB5_NAME = 'System Information Block 5'


def parse_inter_freq_carriers(sib5):
    inter_freq_carriers = []
    for inter_freq_carrier in items_in_tree(sib5, 'interFreqCarrierFreqList', 'InterFreqCarrierFreqInfo_element'):
        inter_freq_cells = []
        if inter_freq_carrier.has_field('interFreqNeighCellList'):
            for cell in items_in_tree(inter_freq_carrier, 'interFreqNeighCellList',
                                      'InterFreqNeighCellInfo_element'):
                inter_freq_cells.append({
                    'physical_cell_id': int(cell.physCellId),
                    'q_offset_cell': Q_OFFSET_RANGE_ENUM[int(cell.q_OffsetCell)],
                })
        inter_freq_carriers.append({
            'dl_carrier_freq': int(inter_freq_carrier.dl_CarrierFreq),
            'q_rx_lev_min': int(inter_freq_carrier.q_RxLevMin) * 2,
            't_reselection_eutra': int(inter_freq_carrier.t_ReselectionEUTRA),
            'thresh_x_high': int(inter_freq_carrier.threshX_High) * 2,
            'thresh_x_low': int(inter_freq_carrier.threshX_Low) * 2,
            'allowed_meas_bandwidth': ALLOWED_MEAS_BANDWIDTH_ENUM[int(inter_freq_carrier.allowedMeasBandwidth)],
            'presence_antenna_port1': inter_freq_carrier.presenceAntennaPort1 != '0',
            'cell_reselection_priority': int(inter_freq_carrier.cellReselectionPriority),
            'neigh_cell_config': NEIGH_CELL_CONFIG_DESC[int(inter_freq_carrier.neighCellConfig)],
            'inter_freq_neigh_cell_list': inter_freq_cells
        })
    return inter_freq_carriers


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib5 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib5_element')
        ][0].sib5_element

        return {
            'event': SIB5_NAME,
            'data': {
                'inter_freq_carriers': parse_inter_freq_carriers(sib5)
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
