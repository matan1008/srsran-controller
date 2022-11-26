RA_RESPONSE_NAME = 'RA Response'


def create(pkt):
    results = []
    mac_layer = pkt['mac-lte']
    if not mac_layer.has_field('rar'):
        return
    rars = mac_layer.body_tree
    if not isinstance(rars, list):
        rars = [rars]
    for rar_body in rars:
        results.append({
            'event': RA_RESPONSE_NAME,
            'ta': int(rar_body.ta),
            'c-rnti': int(rar_body.get_field('temporary-crnti')),
        })
    return results
