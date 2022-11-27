from contextlib import suppress

from .common import ul_nas_msg_container_from_rlc, get_rlcs

GSM_RP_ACK_NAME = 'RP-ACK'
RP_ACK_MESSAGE_TYPE = 2


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            rp = ul_nas_msg_container_from_rlc(rlc).get('gsm_a.rp')
            if int(rp.msg_type, 0) == RP_ACK_MESSAGE_TYPE:
                results.append({
                    'event': GSM_RP_ACK_NAME,
                    'rnti': int(mac_layer.context_tree.rnti),
                    'data': {
                        'message_reference': int(
                            rp.get('RP-Message Reference').get_field('gsm_a.rp.rp_message_reference'), 0
                        ),
                    },
                })
    return results
