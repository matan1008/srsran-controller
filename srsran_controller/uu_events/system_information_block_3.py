from srsran_controller.common.pyshark import items_in_tree
from srsran_controller.uu_events.common import NEIGH_CELL_CONFIG_DESC, ALLOWED_MEAS_BANDWIDTH_ENUM

SIB3_NAME = 'System Information Block 3'

Q_HYST_ENUM = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib3 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib3_element')
        ][0].sib3_element

        serving_info = sib3.cellReselectionServingFreqInfo_element
        intra_freq_info = sib3.intraFreqCellReselectionInfo_element
        data = {
            'q_hyst': Q_HYST_ENUM[int(sib3.cellReselectionInfoCommon_element.q_Hyst)],
            's_non_intra_search': int(serving_info.s_NonIntraSearch) * 2,
            'thresh_serving_low': int(serving_info.threshServingLow) * 2,
            'cell_reselection_priority': int(serving_info.cellReselectionPriority),
            'q_rx_lev_min': int(intra_freq_info.q_RxLevMin) * 2,
            's_intra_search': int(intra_freq_info.s_IntraSearch) * 2,
            'presence_antenna_port1': intra_freq_info.presenceAntennaPort1 != '0',
            'neigh_cell_config': NEIGH_CELL_CONFIG_DESC[int(intra_freq_info.neighCellConfig)],
            't_reselection_eutra': int(intra_freq_info.t_ReselectionEUTRA),
        }

        if intra_freq_info.has_field('allowedMeasBandwidth'):
            data['allowed_meas_bandwidth'] = ALLOWED_MEAS_BANDWIDTH_ENUM[int(intra_freq_info.allowedMeasBandwidth)]

        return {'event': SIB3_NAME, 'data': data}
    except (KeyError, AttributeError, IndexError):
        pass
