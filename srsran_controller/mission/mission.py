import asyncio

from srsran_controller.mission.channel_tracker import ChannelTracker
from srsran_controller.mission.uu_sniffer import UuSniffer
from srsran_controller.uu_events.factory import EventsFactory


class Mission:

    def __init__(self, epc, enb, network):
        """
        Create a new mission object.
        :param srsran_controller.mission.epc.Epc epc: Mission's EPC.
        :param srsran_controller.mission.enb.Enb enb: Mission's ENB.
        :param srsran_controller.mission.lte_network.LteNetwork network: Mission's network.
        """
        self.uu_events = []
        self.uu_events_callback = lambda event: None
        self.channel_tracker = ChannelTracker()
        self._events_factory = EventsFactory(self._handle_uu_event)
        self._sniffer = UuSniffer(self._events_factory, network.INTERFACE_NAME, network.GATEWAY)
        self._sniffing_task = asyncio.create_task(self._sniffer.start())
        self.epc = epc
        self.enb = enb
        self._network = network

    async def stop(self):
        """
        Stop the running mission.
        """
        self._sniffing_task.cancel()
        await self._sniffing_task
        self.enb.shutdown()
        self.epc.shutdown()
        self._network.shutdown()

    def _handle_uu_event(self, event):
        self.uu_events.append(event)
        self.channel_tracker.handle_uu_event(event)
        self.channel_tracker.enrich_event(event)
        self.uu_events_callback(event)
