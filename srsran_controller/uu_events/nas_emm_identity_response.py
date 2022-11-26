from contextlib import suppress

from srsran_controller.common.pyshark import get_field_by_substring
from srsran_controller.uu_events.common import get_rlcs

NAS_EMM_TYPE_IDENTITY_RESPONSE = 0x56
IDENTITY_RESPONSE_NAME = 'Identity response'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            ul = rlc.get('pdcp-lte').lte_rrc.UL_DCCH_Message_element.get('uL_DCCH_Message.message_tree').c1_tree
            ul = ul.ulInformationTransfer_element.criticalExtensions_tree.c1_tree.ulInformationTransfer_r8_element
            ul = ul.dedicatedInfoType_tree.dedicatedInfoNAS_tree.get('nas-eps')
            if int(ul.nas_msg_emm_type, 0) != NAS_EMM_TYPE_IDENTITY_RESPONSE:
                continue

            results.append({
                'imsi': str(get_field_by_substring(ul, 'Mobile identity - IMSI').get_field('e212.imsi')),
                'event': IDENTITY_RESPONSE_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
            })
    return results
