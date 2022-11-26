from contextlib import suppress

from srsran_controller.common.pyshark import get_field_by_substring
from srsran_controller.uu_events.common import get_rlcs

NAS_EMM_TYPE_ATTACH_ACCEPT = 0x42
ATTACH_ACCEPT_NAME = 'Attach accept'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            c = rlc.get('pdcp-lte').lte_rrc.DL_DCCH_Message_element.get('dL_DCCH_Message.message_tree').c1_tree
            c = c.rrcConnectionReconfiguration_element.criticalExtensions_tree.c1_tree
            c = c.rrcConnectionReconfiguration_r8_element.dedicatedInfoNASList_tree.get_field('Item 0')
            c = c.DedicatedInfoNAS_tree.get_field('nas-eps')
            if int(c.nas_msg_emm_type, 0) != NAS_EMM_TYPE_ATTACH_ACCEPT:
                continue
            ip = c.get_field('ESM message container').esm_msg_cont_tree.get_field('PDN address').pdn_ipv4
            results.append({
                'event': ATTACH_ACCEPT_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
                'ip': str(ip),
                'tmsi': int(get_field_by_substring(c, 'Mobile identity - MS identity').get_field('3gpp.tmsi'), 0),
            })
    return results
