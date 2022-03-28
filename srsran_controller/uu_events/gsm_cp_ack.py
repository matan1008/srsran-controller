GSM_CP_ACK_NAME = 'CP-ACK'
SMS_PROTOCOL_DISCRIMINATOR = 9
CP_ACK_MTI = 4


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.gsm_a_dtap_protocol_discriminator) != SMS_PROTOCOL_DISCRIMINATOR:
            return
        if int(mac_layer.gsm_a_dtap_msg_sms_type, 0) == CP_ACK_MTI:
            return {
                'event': GSM_CP_ACK_NAME,
                'rnti': int(mac_layer.rnti),
            }
    except (KeyError, AttributeError):
        pass
