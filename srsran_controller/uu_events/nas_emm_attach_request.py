NAS_EMM_TYPE_ATTACH_REQUEST = 0x41
ATTACH_REQUEST_NAME = 'Attach request'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type) == NAS_EMM_TYPE_ATTACH_REQUEST:
            event = {
                'event': ATTACH_REQUEST_NAME,
                'rnti': int(mac_layer.rnti)
            }
            if hasattr(mac_layer, 'e212.imsi'):
                event['imsi'] = getattr(mac_layer, 'e212.imsi')
            elif hasattr(mac_layer, 'nas_eps.emm.m_tmsi'):
                event['tmsi'] = getattr(mac_layer, 'nas_eps.emm.m_tmsi')
            else:
                # Unknown identity.
                return

            return event
    except (KeyError, AttributeError):
        pass
