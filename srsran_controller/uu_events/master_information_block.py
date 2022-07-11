from srsran_controller.common.pyshark import rrc_get

MIB_NAME = 'Master Information Block'

DL_BANDWIDTH_ENUM = [6, 15, 25, 50, 75, 100]
PHICH_RESOURCE_ENUM = ['1/6', '1/2', '1', '2']


def create(pkt):
    try:
        lte_rrc = pkt['mac-lte'].lte_rrc
        return {
            'event': MIB_NAME,
            'data': {
                'downlink_bandwidth': DL_BANDWIDTH_ENUM[int(rrc_get(lte_rrc, 'dl_Bandwidth'))],
                'phich_duration': 'normal' if rrc_get(lte_rrc, 'phich_Duration') == '0' else 'extended',
                'phich_resource': PHICH_RESOURCE_ENUM[int(rrc_get(lte_rrc, 'phich_Resource'))],
            },
        }
    except (KeyError, AttributeError):
        pass
