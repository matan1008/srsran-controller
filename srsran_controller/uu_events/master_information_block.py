MIB_NAME = 'Master Information Block'

DL_BANDWIDTH_ENUM = [6, 15, 25, 50, 75, 100]
PHICH_RESOURCE_ENUM = ['1/6', '1/2', '1', '2']


def create(pkt):
    try:
        mib = pkt['mac-lte'].lte_rrc.BCCH_BCH_Message_element.message_element
        return {
            'event': MIB_NAME,
            'data': {
                'downlink_bandwidth': DL_BANDWIDTH_ENUM[int(mib.dl_Bandwidth)],
                'phich_duration': 'normal' if mib.phich_Config_element.phich_Duration == '0' else 'extended',
                'phich_resource': PHICH_RESOURCE_ENUM[int(mib.phich_Config_element.phich_Resource)],
            },
        }
    except (KeyError, AttributeError):
        pass
