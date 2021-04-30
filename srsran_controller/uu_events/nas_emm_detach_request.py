NAS_EMM_TYPE_DETACH_REQUEST = 0x45


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type) == NAS_EMM_TYPE_DETACH_REQUEST:
            return {
                'tmsi': mac_layer.nas_eps_emm_m_tmsi,
                'event': 'Detach request',
                'rnti': int(mac_layer.rnti)
            }
    except (KeyError, AttributeError):
        pass
