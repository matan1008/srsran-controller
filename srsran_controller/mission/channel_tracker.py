from dataclasses import dataclass

from srsran_controller.uu_events.nas_emm_attach_request import ATTACH_REQUEST_NAME
from srsran_controller.uu_events.nas_emm_identity_response import IDENTITY_RESPONSE_NAME
from srsran_controller.uu_events.nas_emm_security_mode_complete import SECURITY_MODE_COMPLETE_NAME
from srsran_controller.uu_events.random_access_response import RA_RESPONSE_NAME
from srsran_controller.uu_events.rrc_connection_request import CONNECTION_REQUEST_NAME


@dataclass
class ChannelMetadata:
    ta: int
    imsi: str = ''
    imeisv: str = ''


class ChannelTracker:
    def __init__(self):
        self._rnti_channels = {}
        self._events_handlers = {
            ATTACH_REQUEST_NAME: self._handle_attach_request,
            SECURITY_MODE_COMPLETE_NAME: self._handle_security_mode_complete,
            RA_RESPONSE_NAME: self._handle_rar,
            CONNECTION_REQUEST_NAME: self._handle_connection_request,
            IDENTITY_RESPONSE_NAME: self._handle_identity_response,
        }

    def enrich_event(self, event: dict):
        if 'rnti' not in event:
            return
        channel_metadata = self._rnti_channels[event['rnti']]
        if 'ta' not in event:
            event['ta'] = channel_metadata.ta
        if 'imsi' not in event and channel_metadata.imsi:
            event['imsi'] = channel_metadata.imsi
        if 'imeisv' not in event and channel_metadata.imeisv:
            event['imeisv'] = channel_metadata.imeisv

    def handle_uu_event(self, event: dict) -> None:
        self._events_handlers[event['event']](event)

    def _handle_rar(self, event):
        self._rnti_channels[event['c-rnti']] = ChannelMetadata(ta=event['ta'])

    def _handle_attach_request(self, event):
        self._rnti_channels[event['rnti']].imsi = event['imsi']

    def _handle_security_mode_complete(self, event):
        if 'imeisv' in event:
            self._rnti_channels[event['rnti']].imeisv = event['imeisv']

    def _handle_connection_request(self, event):
        if 'imsi' in event:
            self._rnti_channels[event['rnti']].imsi = event['imsi']

    def _handle_identity_response(self, event):
        if 'imsi' in event:
            self._rnti_channels[event['rnti']].imsi = event['imsi']
