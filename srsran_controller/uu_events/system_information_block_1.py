from srsran_controller.common.pyshark import rrc_get

SIB1_NAME = 'System Information Block 1'


def parse_plmns(lte_rrc):
    plmns = []
    for i in range(int(rrc_get(lte_rrc, 'plmn_IdentityList'))):
        plmns.append({
            'plmn': ''.join(rrc_get(lte_rrc, 'MCC_MNC_Digit')[i * 5: i * 5 + 5]),
            'reserved': rrc_get(lte_rrc, 'cellReservedForOperatorUse')[i] != '1'
        })
    return plmns


def create(pkt):
    try:
        lte_rrc = pkt['mac-lte'].lte_rrc
        if 'lte_rrc_lte-rrc_systemInformationBlockType1_element' not in lte_rrc:
            return
        return {
            'event': SIB1_NAME,
            'data': {
                'plmns': parse_plmns(lte_rrc),
                'tac': int(rrc_get(lte_rrc, 'trackingAreaCode').replace(':', ''), 16),
                'cell_identity': int(rrc_get(lte_rrc, 'cellIdentity').replace(':', ''), 16) >> 4,
                'cell_barred': rrc_get(lte_rrc, 'cellBarred') != '1',
                'intra_freq_reselection': rrc_get(lte_rrc, 'intraFreqReselection') == '0',
                'csg_indication': rrc_get(lte_rrc, 'csg_Indication'),
                'q_rxlevmin': int(rrc_get(lte_rrc, 'q_RxLevMin')) * 2,
                'band': int(rrc_get(lte_rrc, 'freqBandIndicator')),
                'scheduled_sibs': [int(sib) + 3 for sib in rrc_get(lte_rrc, 'SIB_Type')],
            },
        }
    except (KeyError, AttributeError):
        pass
