from dataclasses import dataclass

from srsran_controller.uu_events.nas_emm_attach_accept import ATTACH_ACCEPT_NAME
from srsran_controller.uu_events.nas_emm_attach_request import ATTACH_REQUEST_NAME
from srsran_controller.uu_events.nas_emm_identity_response import IDENTITY_RESPONSE_NAME
from srsran_controller.uu_events.nas_emm_security_mode_complete import SECURITY_MODE_COMPLETE_NAME
from srsran_controller.uu_events.random_access_response import RA_RESPONSE_NAME
from srsran_controller.uu_events.rrc_connection_reestablishment_request import CONNECTION_REESTABLISHMEMT_REQUEST_NAME
from srsran_controller.uu_events.rrc_connection_request import CONNECTION_REQUEST_NAME


@dataclass
class ChannelMetadata:
    ta: int
    imsi: str = ''
    imeisv: str = ''
    ip: str = ''


class ChannelTracker:
    def __init__(self):
        self.rnti_channels = {}
        self._events_handlers = {
            ATTACH_ACCEPT_NAME: self._handle_attach_accept,
            ATTACH_REQUEST_NAME: self._handle_attach_request,
            SECURITY_MODE_COMPLETE_NAME: self._handle_security_mode_complete,
            RA_RESPONSE_NAME: self._handle_rar,
            CONNECTION_REQUEST_NAME: self._handle_connection_request,
            IDENTITY_RESPONSE_NAME: self._handle_identity_response,
            CONNECTION_REESTABLISHMEMT_REQUEST_NAME: self._handle_connection_reesttablishment_request,
        }

    def imsi_to_ip(self, imsi: str) -> str:
        """
        Fetch the last ip seen given to a subscriber.
        :param imsi: Subscriber's IMSI.
        :return: Subscriber's IP.
        """
        for channel in self.rnti_channels.values():
            if channel.imsi == imsi:
                return channel.ip

    def get_channel(self, enb_ip: str, rnti: int) -> ChannelMetadata:
        """
        Get channel's metadate.
        :param enb_ip: IP of enb.
        :param rnti: C-RNTI of the request channel.
        :return: All known metadata about the channel.
        """
        return self.rnti_channels[(enb_ip, rnti)]

    def enrich_event(self, event: dict) -> None:
        """
        Add additional data to a Uu event, based on the RNTI.
        :param event: Uu event to add data to.
        """
        if 'rnti' not in event:
            return
        channel_metadata = self.rnti_channels[event['enb_ip'], event['rnti']]
        if 'ta' not in event:
            event['ta'] = channel_metadata.ta
        if 'imsi' not in event and channel_metadata.imsi:
            event['imsi'] = channel_metadata.imsi
        if 'imeisv' not in event and channel_metadata.imeisv:
            event['imeisv'] = channel_metadata.imeisv
        if 'ip' not in event and channel_metadata.ip:
            event['ip'] = channel_metadata.ip

    def handle_uu_event(self, event: dict) -> None:
        """
        Cache possible data from an event on the Uu interface
        :param event: Uu event to extract data from.
        """
        if event['event'] not in self._events_handlers:
            return
        self._events_handlers[event['event']](event)

    def _handle_rar(self, event: dict):
        self.rnti_channels[event['enb_ip'], event['c-rnti']] = ChannelMetadata(ta=event['ta'])

    def _handle_attach_accept(self, event: dict):
        self.rnti_channels[event['enb_ip'], event['rnti']].ip = event['ip']
        self._set_imsi(event)

    def _handle_attach_request(self, event: dict):
        self._set_imsi(event)

    def _handle_security_mode_complete(self, event: dict):
        if 'imeisv' in event:
            self.rnti_channels[event['enb_ip'], event['rnti']].imeisv = event['imeisv']

    def _handle_connection_request(self, event: dict):
        self._set_imsi(event)

    def _handle_identity_response(self, event: dict):
        self._set_imsi(event)

    def _handle_connection_reesttablishment_request(self, event: dict):
        # Todo: Better check for source enb
        old_channel = (event['enb_ip'], event['c-rnti'])
        if old_channel not in self.rnti_channels:
            return
        self.rnti_channels[event['enb_ip'], event['rnti']] = self.rnti_channels.pop(old_channel)

    def _set_imsi(self, event: dict):
        if 'imsi' not in event:
            return
        new_chan = (event['enb_ip'], event['rnti'])
        self.rnti_channels[new_chan].imsi = event['imsi']
        # Remove old channels related to this imsi.
        for old_chan in list(self.rnti_channels.keys()):
            if self.rnti_channels[old_chan].imsi == event['imsi'] and old_chan != new_chan:
                if self.rnti_channels[old_chan].imeisv and not self.rnti_channels[new_chan].imeisv:
                    self.rnti_channels[new_chan].imeisv = self.rnti_channels[old_chan].imeisv
                if self.rnti_channels[old_chan].ip and not self.rnti_channels[new_chan].ip:
                    self.rnti_channels[new_chan].ip = self.rnti_channels[old_chan].ip
                del self.rnti_channels[old_chan]
