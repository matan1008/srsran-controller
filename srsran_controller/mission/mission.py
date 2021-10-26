import asyncio
from datetime import datetime
from logging import Logger, getLogger

from srsran_controller.mission.channel_tracker import ChannelTracker
from srsran_controller.mission.ping import Ping
from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.uu_sniffer import UuSniffer


class Mission:

    def __init__(self, epc, enb, lte_network, pgw_network=None, logger: Logger = getLogger('srsran_controller')):
        """
        Create a new mission object.
        :param srsran_controller.mission.epc.Epc epc: Mission's EPC.
        :param srsran_controller.mission.enb.Enb enb: Mission's ENB.
        :param srsran_controller.mission.lte_network.LteNetwork lte_network: Mission's network.
        :param srsran_controller.mission.pgw_network.PgwNetwork pgw_network: P-GW network.
        :param logger: Logger.
        """
        self.uu_events = []
        self.uu_events_callback = lambda event: None
        self.ping_status_callback = lambda ping: None
        self.ping_log_callback = lambda ping, time, log: None
        self.channel_tracker = ChannelTracker()
        self.epc = epc
        self.enb = enb
        self._lte_network = lte_network
        self._pgw_network = pgw_network
        self.logger = logger
        self.pings = []
        self.start_time = datetime.now()
        self._sniffing_task = asyncio.create_task(self._sniff_packets())

    async def ping(self, imsi: str) -> Ping:
        """
        Ping a UE.
        :param imsi: UE's IMSI.
        :return: Ping object.
        """
        ip = self.channel_tracker.imsi_to_ip(imsi)
        ping = await Ping.create(self.epc, ip, imsi, self._handle_ping_status, self._handle_ping_log)
        self.pings.append(ping)
        return ping

    async def stop_ping(self, id_: str) -> None:
        """
        Stop a running ping.
        :param id_: Ping ID.
        """
        for ping in self.pings:
            if not ping.stopped and ping.id == id_:
                await ping.stop()

    async def stop(self):
        """
        Stop the running mission.
        """
        await asyncio.gather(*[ping.stop() for ping in self.pings if not ping.stopped])
        self._sniffing_task.cancel()
        await self._sniffing_task
        self.enb.shutdown()
        self.epc.shutdown()
        self._lte_network.shutdown()
        if self._pgw_network is not None:
            self._pgw_network.shutdown()

    async def _sniff_packets(self):
        events_factory = EventsFactory()
        sniffer = UuSniffer(self._lte_network.INTERFACE_NAME, self._lte_network.GATEWAY)
        async for packet in sniffer.start():
            for event in events_factory.from_packet(packet):
                self._handle_uu_event(event)

    def _handle_uu_event(self, event):
        self.logger.debug(f'Handle Uu event: {event}')
        self.uu_events.append(event)
        self.channel_tracker.handle_uu_event(event)
        self.channel_tracker.enrich_event(event)
        self.uu_events_callback(event)

    def _handle_ping_status(self, ping: Ping):
        self.ping_status_callback(ping)

    def _handle_ping_log(self, ping: Ping, time: datetime, log: str):
        self.ping_log_callback(ping, time, log)
