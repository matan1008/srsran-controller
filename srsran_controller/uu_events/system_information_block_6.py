from srsran_controller.common.pyshark import items_in_tree

SIB6_NAME = 'System Information Block 6'


def parse_fdd_carrier_freq_utras(sib6):
    fdd_carrier_freq_utras = []
    for carrier_freq_element in items_in_tree(sib6, 'carrierFreqListUTRA_FDD', 'CarrierFreqUTRA_FDD_element'):
        fdd_carrier_freq_utras.append({
            'carrier_freq': int(carrier_freq_element.carrierFreq),
            'cell_reselection_priority': int(carrier_freq_element.cellReselectionPriority),
            'thresh_x_high': int(carrier_freq_element.threshX_High) * 2,
            'thresh_x_low': int(carrier_freq_element.threshX_Low) * 2,
            'q_rx_lev_min': int(carrier_freq_element.utra_q_RxLevMin) * 2 + 1,
            'p_max_utra': int(carrier_freq_element.p_MaxUTRA),
            'q_qual_min': int(carrier_freq_element.q_QualMin),
        })
    return fdd_carrier_freq_utras


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib6 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib6_element')
        ][0].sib6_element

        return {
            'event': SIB6_NAME,
            'data': {
                'utra_fdd_carriers': parse_fdd_carrier_freq_utras(sib6),
                't_reselection_utra': int(sib6.t_ReselectionUTRA),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
