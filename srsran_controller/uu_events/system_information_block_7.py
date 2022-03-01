from srsran_controller.common.pyshark import items_in_tree

SIB7_NAME = 'System Information Block 7'
BAND_INDICATORS = ['dcs1800', 'pcs1900', '']


def parse_carrier_freqs(sib7):
    carrier_freqs = []
    for carrier_freq_element in items_in_tree(sib7, 'carrierFreqsInfoList', 'CarrierFreqsInfoGERAN_element'):
        carrier_freqs.append({
            'starting_arfcn': int(carrier_freq_element.carrierFreqs_element.startingARFCN),
            'band_indicator': BAND_INDICATORS[int(carrier_freq_element.carrierFreqs_element.bandIndicator)],
            'cell_reselection_priority': int(carrier_freq_element.commonInfo_element.cellReselectionPriority),
            'ncc_permitted': int(carrier_freq_element.commonInfo_element.ncc_Permitted, 16),
            'thresh_x_high': int(carrier_freq_element.commonInfo_element.threshX_High) * 2,
            'thresh_x_low': int(carrier_freq_element.commonInfo_element.threshX_Low) * 2,
            'q_rx_lev_min': int(carrier_freq_element.commonInfo_element.geran_q_RxLevMin) * 2 - 115,
        })
    return carrier_freqs


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib7 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib7_element')
        ][0].sib7_element

        return {
            'event': SIB7_NAME,
            'data': {
                'carrier_freqs': parse_carrier_freqs(sib7),
                't_reselection_geran': int(sib7.t_ReselectionGERAN),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
