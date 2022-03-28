GSM_RP_ACK_NAME = 'RP-ACK'
RP_ACK_MESSAGE_TYPE = 2


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.gsm_a_rp_msg_type, 0) == RP_ACK_MESSAGE_TYPE:
            return {
                'event': GSM_RP_ACK_NAME,
                'rnti': int(mac_layer.rnti),
                'data': {
                    'message_reference': int(mac_layer.gsm_a_rp_rp_message_reference, 0),
                },
            }
    except (KeyError, AttributeError):
        pass
