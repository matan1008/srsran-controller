from datetime import datetime

from srslte_controller.uu_events.nas_emm_attach_request import create as create_attach_request
from srslte_controller.uu_events.random_access_response import create as create_ra_response


class EventsFactory:

    def __init__(self, callback):
        self.callback = callback
        self.events_creators = [
            create_attach_request,
            create_ra_response,
        ]

    def from_packet(self, pkt):
        for creator in self.events_creators:
            if (event := creator(pkt)) is not None:
                event['time'] = datetime.fromtimestamp(float(pkt.frame_info.time_epoch))
                self.callback(event)
