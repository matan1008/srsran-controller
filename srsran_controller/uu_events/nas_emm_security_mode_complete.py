from contextlib import suppress

from srsran_controller.common.pyshark import get_field_by_substring
from srsran_controller.uu_events.common import get_rlcs, ul_nas_eps_from_rlc

NAS_EMM_TYPE_SECURITY_MODE_COMPLETE = 0x5e
SECURITY_MODE_COMPLETE_NAME = 'Security mode complete'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            ul = ul_nas_eps_from_rlc(rlc)
            if int(ul.nas_msg_emm_type, 0) != NAS_EMM_TYPE_SECURITY_MODE_COMPLETE:
                continue

            event = {
                'event': SECURITY_MODE_COMPLETE_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
            }
            if (identity := get_field_by_substring(ul, 'Mobile identity - IMEISV')) is not None:
                event['imeisv'] = identity.get_field('gsm_a.imeisv')
            results.append(event)
    return results
