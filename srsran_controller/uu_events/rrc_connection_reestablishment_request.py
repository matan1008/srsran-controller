REESTABLISHMENT_REQUEST_TAG = 'lte_rrc_rrCconnectionReestablishmentRequest_r8_element'
CONNECTION_REESTABLISHMEMT_REQUEST_NAME = 'RRC connection reestablishment request'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if not hasattr(mac_layer, REESTABLISHMENT_REQUEST_TAG):
            return
        return {
            'event': CONNECTION_REESTABLISHMEMT_REQUEST_NAME,
            'physical_cell_id': int(mac_layer.lte_rrc_physcellid),
            'rnti': int(mac_layer.rnti),
            'c-rnti': int(mac_layer.lte_rrc_c_rnti.replace(':', ''), 16)
        }
    except (KeyError, AttributeError):
        pass
