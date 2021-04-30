NAS_EMM_TYPE_ATTACH_REQUEST = 0x41


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type) == NAS_EMM_TYPE_ATTACH_REQUEST:
            return {
                'imsi': getattr(mac_layer, 'e212.imsi'),
                'event': 'Attach request',
                'rnti': int(mac_layer.rnti)
            }
    except (KeyError, AttributeError):
        pass
