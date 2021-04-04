def create(pkt):
    try:
        mac_layer = pkt['mac-lte']
        return {
            'event': 'RA Response',
            'ta': int(mac_layer.rar_ta),
            'c-rnti': int(mac_layer.rar_temporary_crnti),
        }
    except (KeyError, AttributeError):
        pass
