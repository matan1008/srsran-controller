from srsran_controller.common.pyshark import rrc_get

SIB2_NAME = 'System Information Block 2'

PREAMBLE_TRANS_MAX_ENUM = [3, 4, 5, 6, 7, 8, 10, 20, 50, 100, 200]
RA_RESPONSE_WINDOW_SIZE = [2, 3, 4, 5, 6, 7, 8, 10]


def create(pkt):
    try:
        lte_rrc = pkt['mac-lte'].lte_rrc
        if 'lte_rrc_lte-rrc_sib2_element' not in lte_rrc:
            return

        return {
            'event': SIB2_NAME,
            'data': {
                'number_of_ra_preambles': int(rrc_get(lte_rrc, 'numberOfRA_Preambles')) * 4 + 4,
                'power_ramping_step': int(rrc_get(lte_rrc, 'powerRampingStep')) * 2,
                'preamble_initial_received_target_power': int(
                    rrc_get(lte_rrc, 'preambleInitialReceivedTargetPower')) * 2 - 120,
                'preamble_trans_max': PREAMBLE_TRANS_MAX_ENUM[int(rrc_get(lte_rrc, 'preambleTransMax'))],
                'ra_response_window_size': RA_RESPONSE_WINDOW_SIZE[int(rrc_get(lte_rrc, 'ra_ResponseWindowSize'))],
                'mac_contention_resolution_timer': int(rrc_get(lte_rrc, 'mac_ContentionResolutionTimer')) * 8 + 8,
                'max_harq_msg3_tx': int(rrc_get(lte_rrc, 'maxHARQ_Msg3Tx')),
                'modification_period_coeff': 2 ** (int(rrc_get(lte_rrc, 'modificationPeriodCoeff')) + 1),
            },
        }
    except (KeyError, AttributeError, IndexError):
        pass
