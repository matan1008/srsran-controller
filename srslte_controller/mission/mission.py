import asyncio

from srslte_controller.configuration import config
from srslte_controller.mission.uu_sniffer import UuSniffer
from srslte_controller.uu_events.factory import EventsFactory


class Mission:

    def __init__(self, epc, enb, network):
        """
        Create a new mission object.
        :param srslte_controller.mission.epc.Epc epc: Mission's EPC.
        :param srslte_controller.mission.enb.Enb enb: Mission's ENB.
        :param srslte_controller.mission.lte_network.LteNetwork network: Mission's network.
        """
        self.uu_events = []
        self._events_factory = EventsFactory(self.uu_events.append)
        self._sniffer = UuSniffer(config.current_enb_cap, self._events_factory)
        self._sniffing_task = asyncio.create_task(self._sniffer.start())
        self.epc = epc
        self.enb = enb
        self._network = network

    async def stop(self):
        """
        Stop the running mission.
        """
        self._sniffer.stop()
        await self._sniffing_task
        self.enb.shutdown()
        self.epc.shutdown()
        self._network.shutdown()
