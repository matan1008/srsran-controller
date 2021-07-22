from datetime import datetime

from srsran_controller.uu_events.nas_emm_attach_request import create as create_attach_request
from srsran_controller.uu_events.nas_emm_detach_request import create as create_detach_request
from srsran_controller.uu_events.nas_emm_identity_response import create as create_identity_response
from srsran_controller.uu_events.nas_emm_security_mode_complete import create as create_security_mode_complete
from srsran_controller.uu_events.random_access_response import create as create_ra_response
from srsran_controller.uu_events.rrc_connection_request import create as create_rrc_conn_request


class EventsFactory:

    def __init__(self, callback):
        self.callback = callback
        self.events_creators = [
            create_attach_request,
            create_detach_request,
            create_identity_response,
            create_security_mode_complete,
            create_ra_response,
            create_rrc_conn_request,
        ]

    def from_packet(self, pkt):
        for creator in self.events_creators:
            if (event := creator(pkt)) is not None:
                event['time'] = datetime.fromtimestamp(float(pkt.frame_info.time_epoch))
                self.callback(event)
