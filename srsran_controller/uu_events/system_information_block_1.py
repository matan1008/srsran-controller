from srsran_controller.common.pyshark import items_in_tree

SIB1_NAME = 'System Information Block 1'


def parse_plmns(cell_access):
    plmns = []
    for plmn_identity in items_in_tree(cell_access, 'plmn_IdentityList', 'PLMN_IdentityInfo_element'):
        reserved = plmn_identity.cellReservedForOperatorUse != '1'
        plmn_identity = plmn_identity.plmn_Identity_element
        mcc = ''.join(str(digit) for digit in items_in_tree(plmn_identity, 'mcc', 'MCC_MNC_Digit'))
        mnc = ''.join(str(digit) for digit in items_in_tree(plmn_identity, 'mnc', 'MCC_MNC_Digit'))
        plmns.append({
            'plmn': mcc + mnc,
            'reserved': reserved
        })
    return plmns


def parse_scheduled_sibs(sib1):
    scheduled_sibs = []
    for scheduling_info in items_in_tree(sib1, 'schedulingInfoList', 'SchedulingInfo_element'):
        for sib in items_in_tree(scheduling_info, 'sib_MappingInfo', 'SIB_Type'):
            scheduled_sibs.append(int(sib) + 3)
    return scheduled_sibs


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sib1 = c1.systemInformationBlockType1_element
        cell_access = sib1.cellAccessRelatedInfo_element
        cell_selection = sib1.cellSelectionInfo_element
        return {
            'event': SIB1_NAME,
            'data': {
                'plmns': parse_plmns(cell_access),
                'tac': int(cell_access.trackingAreaCode.replace(':', ''), 16),
                'cell_identity': int(cell_access.cellIdentity.replace(':', ''), 16) >> 4,
                'cell_barred': cell_access.cellBarred != '1',
                'intra_freq_reselection': cell_access.intraFreqReselection == '0',
                'csg_indication': cell_access.csg_Indication != '0',
                'q_rxlevmin': int(cell_selection.q_RxLevMin) * 2,
                'band': int(sib1.freqBandIndicator),
                'scheduled_sibs': parse_scheduled_sibs(sib1),
            },
        }
    except (KeyError, AttributeError):
        pass
