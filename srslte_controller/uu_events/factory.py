from datetime import datetime


class EventsFactory:
    NAS_EMM_TYPE_ATTACH_REQUEST = 0x41

    def __init__(self, callback):
        self.callback = callback

    def from_packet(self, pkt):
        try:
            mac_layer = pkt['mac-lte']
            if int(mac_layer.nas_eps_nas_msg_emm_type) == self.NAS_EMM_TYPE_ATTACH_REQUEST:
                self.callback({
                    'imsi': getattr(mac_layer, 'e212.imsi'),
                    'event': 'Attach request',
                    'time': datetime.fromtimestamp(float(pkt.frame_info.time_epoch))
                })
        except (KeyError, AttributeError):
            pass
