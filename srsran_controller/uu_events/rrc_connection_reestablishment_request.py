from contextlib import suppress

REESTABLISHMENT_REQUEST_TAG = 'lte_rrc_rrCconnectionReestablishmentRequest_r8_element'
CONNECTION_REESTABLISHMEMT_REQUEST_NAME = 'RRC connection reestablishment request'


def create(pkt):
    with suppress(KeyError, AttributeError):
        mac_layer = pkt['mac-lte']
        ul = mac_layer.lte_rrc.UL_CCCH_Message_element.message_tree.c1_tree.rrcConnectionReestablishmentRequest_element
        ul = ul.criticalExtensions_tree.rrcConnectionReestablishmentRequest_r8_element.ue_Identity_element
        return {
            'event': CONNECTION_REESTABLISHMEMT_REQUEST_NAME,
            'rnti': int(mac_layer.context_tree.rnti),
            'physical_cell_id': int(ul.physCellId),
            'c-rnti': int(ul.c_RNTI.replace(':', ''), 16)
        }
