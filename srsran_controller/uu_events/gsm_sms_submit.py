TP_MTI_SMS_SUBMIT = 1
GSM_SMS_SUBMIT_NAME = 'SMS Submit'


def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        if int(mac_layer.gsm_sms_tp_mti) == TP_MTI_SMS_SUBMIT:
            return {
                'event': GSM_SMS_SUBMIT_NAME,
                'rnti': int(mac_layer.rnti),
                'data': {
                    'rp_da': str(mac_layer.gsm_a_dtap_cld_party_bcd_num),
                    'tp_da': str(mac_layer.gsm_sms_tp_da),
                    'content': str(mac_layer.gsm_sms_sms_text),
                }
            }
    except (KeyError, AttributeError):
        pass
