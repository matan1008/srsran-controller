NAS_EMM_TYPE_IDENTITY_RESPONSE = 0x56
IDENTITY_RESPONSE_NAME = 'Identity response'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.nas_eps_nas_msg_emm_type) == NAS_EMM_TYPE_IDENTITY_RESPONSE:
            return {
                'imsi': getattr(mac_layer, 'e212.imsi'),
                'event': IDENTITY_RESPONSE_NAME,
                'rnti': int(mac_layer.rnti)
            }
    except (KeyError, AttributeError):
        pass
