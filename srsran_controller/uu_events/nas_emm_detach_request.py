from contextlib import suppress

from srsran_controller.uu_events.common import get_rlcs, ul_nas_eps_from_rlc

NAS_EMM_TYPE_DETACH_REQUEST = 0x45
DETACH_REQUEST_NAME = 'Detach request'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            ul = ul_nas_eps_from_rlc(rlc)
            if int(ul.nas_msg_emm_type, 0) != NAS_EMM_TYPE_DETACH_REQUEST:
                continue

            results.append({
                'tmsi': int(ul.get_field('EPS mobile identity').get_field('3gpp.tmsi'), 0),
                'event': DETACH_REQUEST_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
            })
    return results
