from srsran_controller.common.pyshark import rrc_get
from srsran_controller.uu_events.common import NEIGH_CELL_CONFIG_DESC, ALLOWED_MEAS_BANDWIDTH_ENUM

SIB3_NAME = 'System Information Block 3'

Q_HYST_ENUM = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]


def create(pkt):
    try:
        lte_rrc = pkt['mac-lte'].lte_rrc
        if 'lte_rrc_lte-rrc_sib3_element' not in lte_rrc:
            return

        data = {
            'q_hyst': Q_HYST_ENUM[int(rrc_get(lte_rrc, 'q_Hyst'))],
            's_non_intra_search': int(rrc_get(lte_rrc, 's_NonIntraSearch')) * 2,
            'thresh_serving_low': int(rrc_get(lte_rrc, 'threshServingLow')) * 2,
            'cell_reselection_priority': int(rrc_get(lte_rrc, 'cellReselectionPriority')),
            'q_rx_lev_min': int(rrc_get(lte_rrc, 'q_RxLevMin')) * 2,
            's_intra_search': int(rrc_get(lte_rrc, 's_IntraSearch')) * 2,
            'presence_antenna_port1': rrc_get(lte_rrc, 'presenceAntennaPort1'),
            'neigh_cell_config': NEIGH_CELL_CONFIG_DESC[int(rrc_get(lte_rrc, 'neighCellConfig'))],
            't_reselection_eutra': int(rrc_get(lte_rrc, 't_ReselectionEUTRA')),
        }

        try:
            data['allowed_meas_bandwidth'] = ALLOWED_MEAS_BANDWIDTH_ENUM[int(rrc_get(lte_rrc, 'allowedMeasBandwidth'))]
        except KeyError:
            pass

        return {'event': SIB3_NAME, 'data': data}
    except (KeyError, AttributeError, IndexError):
        pass
