from srsran_controller.common.pyshark import items_in_tree

SIB2_NAME = 'System Information Block 2'

PREAMBLE_TRANS_MAX_ENUM = [3, 4, 5, 6, 7, 8, 10, 20, 50, 100, 200]
RA_RESPONSE_WINDOW_SIZE = [2, 3, 4, 5, 6, 7, 8, 10]


def create(pkt):
    try:
        c1 = pkt['mac-lte'].lte_rrc.BCCH_DL_SCH_Message_element.message_tree.c1_tree
        sys_info_element = c1.systemInformation_element.criticalExtensions_tree.systemInformation_r8_element
        sib2 = [
            sib
            for sib
            in items_in_tree(sys_info_element, 'sib_TypeAndInfo', 'sib_TypeAndInfo_item_tree')
            if sib.has_field('sib2_element')
        ][0].sib2_element
        rr_config = sib2.radioResourceConfigCommon_element
        rach_common = rr_config.rach_ConfigCommon_element
        power_ramp = rach_common.powerRampingParameters_element
        ra_supervision = rach_common.ra_SupervisionInfo_element
        return {
            'event': SIB2_NAME,
            'data': {
                'number_of_ra_preambles': int(rach_common.preambleInfo_element.numberOfRA_Preambles) * 4 + 4,
                'power_ramping_step': int(power_ramp.powerRampingStep) * 2,
                'preamble_initial_received_target_power': int(power_ramp.preambleInitialReceivedTargetPower) * 2 - 120,
                'preamble_trans_max': PREAMBLE_TRANS_MAX_ENUM[int(ra_supervision.preambleTransMax)],
                'ra_response_window_size': RA_RESPONSE_WINDOW_SIZE[int(ra_supervision.ra_ResponseWindowSize)],
                'mac_contention_resolution_timer': int(ra_supervision.mac_ContentionResolutionTimer) * 8 + 8,
                'max_harq_msg3_tx': int(rach_common.maxHARQ_Msg3Tx),
                'modification_period_coeff': 2 ** (int(rr_config.bcch_Config_element.modificationPeriodCoeff) + 1),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
