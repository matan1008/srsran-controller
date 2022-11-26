from contextlib import suppress

from srsran_controller.common.pyshark import get_field_by_substring
from srsran_controller.uu_events.common import ul_nas_msg_container_from_rlc, get_rlcs

TP_MTI_SMS_SUBMIT = 1
GSM_SMS_SUBMIT_NAME = 'SMS Submit'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            nas = ul_nas_msg_container_from_rlc(rlc)
            sms = nas.gsm_sms
            if int(sms.get_field('tp-mti')) != TP_MTI_SMS_SUBMIT:
                continue
            results.append({
                'event': GSM_SMS_SUBMIT_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
                'data': {
                    'rp_da': str(get_field_by_substring(nas.rp, 'RP-Destination Address').cld_party_bcd_num),
                    'tp_da': str(get_field_by_substring(sms, 'TP-Destination-Address').get_field('tp-da')),
                    'content': sms.get_field('TP-User-Data').sms_text,
                }
            })
    return results
