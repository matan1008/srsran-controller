RRC_CONNECTION_REQUEST_TAG = 'lte_rrc_rrcconnectionrequest_element'
RRC_TMSI_TAG = 'lte_rrc_m_tmsi'
CONNECTION_REQUEST_NAME = 'RRC connection request'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if not hasattr(mac_layer, RRC_CONNECTION_REQUEST_TAG):
            return
        identity = {}
        if hasattr(mac_layer, RRC_TMSI_TAG):
            identity = {'tmsi': mac_layer.lte_rrc_m_tmsi.hex_value}
        if not identity:
            return
        event = {
            'event': CONNECTION_REQUEST_NAME,
            'rnti': int(mac_layer.rnti)
        }
        event.update(identity)
        return event
    except (KeyError, AttributeError):
        pass
