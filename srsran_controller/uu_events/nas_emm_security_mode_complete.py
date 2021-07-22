NAS_EMM_TYPE_SECURITY_MODE_COMPLETE = 0x5e


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type) == NAS_EMM_TYPE_SECURITY_MODE_COMPLETE:
            event = {
                'event': 'Security mode complete',
                'rnti': int(mac_layer.rnti),
            }
            if hasattr(mac_layer, 'gsm_a.imeisv'):
                event['imeisv'] = getattr(mac_layer, 'gsm_a.imeisv')
            return event
    except (KeyError, AttributeError):
        pass
