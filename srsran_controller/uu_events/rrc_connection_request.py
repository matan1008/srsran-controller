from contextlib import suppress

RRC_CONNECTION_REQUEST_TAG = 'lte_rrc_rrcconnectionrequest_element'
RRC_TMSI_TAG = 'lte_rrc_m_tmsi'
CONNECTION_REQUEST_NAME = 'RRC connection request'


def create(pkt):
    with suppress(KeyError, AttributeError):
        mac_layer = pkt['mac-lte']
        ul = mac_layer.lte_rrc.UL_CCCH_Message_element.message_tree.c1_tree.rrcConnectionRequest_element
        ul = ul.criticalExtensions_tree.rrcConnectionRequest_r8_element.ue_Identity_tree
        return {
            'event': CONNECTION_REQUEST_NAME,
            'rnti': int(mac_layer.context_tree.rnti),
            'tmsi': int(ul.s_TMSI_element.m_TMSI.replace(':', ''), 16),
        }
