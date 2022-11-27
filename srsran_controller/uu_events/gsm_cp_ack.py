from contextlib import suppress

from srsran_controller.uu_events.common import ul_nas_msg_container_from_rlc, get_rlcs

GSM_CP_ACK_NAME = 'CP-ACK'
SMS_PROTOCOL_DISCRIMINATOR = 9
CP_ACK_MTI = 4


def _is_cp_ack(dtap):
    return int(dtap.protocol_discriminator) == SMS_PROTOCOL_DISCRIMINATOR and int(dtap.msg_sms_type, 0) == CP_ACK_MTI


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            dtap = ul_nas_msg_container_from_rlc(rlc).get('gsm_a.dtap')
            if _is_cp_ack(dtap):
                results.append({
                    'event': GSM_CP_ACK_NAME,
                    'rnti': int(mac_layer.context_tree.rnti),
                })
    return results
