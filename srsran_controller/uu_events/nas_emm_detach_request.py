NAS_EMM_TYPE_DETACH_REQUEST = 0x45
DETACH_REQUEST_NAME = 'Detach request'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type, 0) == NAS_EMM_TYPE_DETACH_REQUEST:
            return {
                'tmsi': int(mac_layer.nas_eps_emm_m_tmsi, 0),
                'event': DETACH_REQUEST_NAME,
                'rnti': int(mac_layer.rnti)
            }
    except (KeyError, AttributeError):
        pass
