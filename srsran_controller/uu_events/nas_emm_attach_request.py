NAS_EMM_TYPE_ATTACH_REQUEST = 0x41
ATTACH_REQUEST_NAME = 'Attach request'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type, 0) != NAS_EMM_TYPE_ATTACH_REQUEST:
            return

        event = {
            'event': ATTACH_REQUEST_NAME,
            'rnti': int(mac_layer.rnti)
        }
        if hasattr(mac_layer, 'e212.imsi'):
            event['imsi'] = getattr(mac_layer, 'e212.imsi')
        elif hasattr(mac_layer, 'nas_eps.emm.m_tmsi'):
            event['tmsi'] = int(mac_layer.nas_eps_emm_m_tmsi, 0)
        else:
            # Unknown identity.
            return

        data = {}
        if hasattr(mac_layer, 'nas_eps.emm.tai_tac'):
            data['old_tai'] = {
                'mcc': '{:>03}'.format(getattr(mac_layer, 'e212.tai.mcc')),
                'mnc': '{:>02}'.format(getattr(mac_layer, 'e212.tai.mnc')),
                'tac': int(getattr(mac_layer, 'nas_eps.emm.tai_tac')),
            }
        if hasattr(mac_layer, 'gsm_a.lac'):
            data['old_lai'] = {
                'mcc': '{:>03}'.format(getattr(mac_layer, 'e212.lai.mcc')),
                'mnc': '{:>02}'.format(getattr(mac_layer, 'e212.lai.mnc')),
                'lac': int(getattr(mac_layer, 'gsm_a.lac'), 0),
            }

        event['data'] = data

        return event
    except (KeyError, AttributeError):
        pass
