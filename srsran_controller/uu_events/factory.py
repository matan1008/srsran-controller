from datetime import datetime

from srsran_controller.uu_events.gsm_sms_submit import create as create_gsm_sms_submit
from srsran_controller.uu_events.master_information_block import create as create_mib
from srsran_controller.uu_events.nas_emm_attach_accept import create as create_attach_accept
from srsran_controller.uu_events.nas_emm_attach_request import create as create_attach_request
from srsran_controller.uu_events.nas_emm_detach_request import create as create_detach_request
from srsran_controller.uu_events.nas_emm_identity_response import create as create_identity_response
from srsran_controller.uu_events.nas_emm_security_mode_complete import create as create_security_mode_complete
from srsran_controller.uu_events.random_access_response import create as create_ra_response
from srsran_controller.uu_events.rrc_connection_reestablishment_request import create as create_rrc_conn_reest_req
from srsran_controller.uu_events.rrc_connection_request import create as create_rrc_conn_request
from srsran_controller.uu_events.system_information_block_1 import create as create_sib1
from srsran_controller.uu_events.system_information_block_2 import create as create_sib2
from srsran_controller.uu_events.system_information_block_3 import create as create_sib3
from srsran_controller.uu_events.system_information_block_4 import create as create_sib4
from srsran_controller.uu_events.system_information_block_5 import create as create_sib5
from srsran_controller.uu_events.system_information_block_6 import create as create_sib6
from srsran_controller.uu_events.system_information_block_7 import create as create_sib7


class EventsFactory:

    def __init__(self):
        self.events_creators = [
            create_gsm_sms_submit,
            create_mib,
            create_attach_accept,
            create_attach_request,
            create_detach_request,
            create_identity_response,
            create_security_mode_complete,
            create_ra_response,
            create_rrc_conn_reest_req,
            create_rrc_conn_request,
            create_sib1,
            create_sib2,
            create_sib3,
            create_sib4,
            create_sib5,
            create_sib6,
            create_sib7,
        ]

    def from_packet(self, pkt):
        for creator in self.events_creators:
            if (event := creator(pkt)) is not None:
                event['time'] = datetime.fromtimestamp(float(pkt.frame_info.time_epoch))
                yield event
