from contextlib import suppress

from srsran_controller.common.pyshark import get_field_by_substring
from srsran_controller.uu_events.common import get_rlcs

NAS_EMM_TYPE_ATTACH_REQUEST = 0x41
ATTACH_REQUEST_NAME = 'Attach request'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    for rlc in get_rlcs(mac_layer):
        with suppress(KeyError, AttributeError):
            ul = rlc.get('pdcp-lte').lte_rrc.UL_DCCH_Message_element.get('uL_DCCH_Message.message_tree').c1_tree
            ul = ul.rrcConnectionSetupComplete_element.criticalExtensions_tree.c1_tree
            ul = ul.rrcConnectionSetupComplete_r8_element.dedicatedInfoNAS_tree.get_field('nas-eps')
            if int(ul.nas_msg_emm_type, 0) != NAS_EMM_TYPE_ATTACH_REQUEST:
                continue

            event = {
                'event': ATTACH_REQUEST_NAME,
                'rnti': int(mac_layer.context_tree.rnti),
                'data': {},
            }
            identity = ul.get_field('EPS mobile identity')
            if (imsi := identity.get('e212.imsi')) is not None:
                event['imsi'] = str(imsi)
            if (tmsi := identity.get('3gpp.tmsi')) is not None:
                event['tmsi'] = int(tmsi, 0)

            if (old_tai := ul.get('Tracking area identity - Last visited registered TAI')) is not None:
                event['data']['old_tai'] = {
                    'mcc': '{:>03}'.format(old_tai.get_field('e212.tai.mcc')),
                    'mnc': '{:>02}'.format(old_tai.get_field('e212.tai.mnc')),
                    'tac': int(old_tai.get_field('nas_eps.emm.tai_tac')),
                }
            if (old_lai := ul.get('Location area identification - Old location area identification')) is not None:
                old_lai = get_field_by_substring(old_lai, 'Location Area Identification (LAI)')
                event['data']['old_lai'] = {
                    'mcc': '{:>03}'.format(old_lai.get_field('e212.lai.mcc')),
                    'mnc': '{:>02}'.format(old_lai.get_field('e212.lai.mnc')),
                    'lac': int(old_lai.get_field('gsm_a.lac'), 0),
                }
            results.append(event)

    return results
