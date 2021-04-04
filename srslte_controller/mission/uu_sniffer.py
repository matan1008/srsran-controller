import asyncio
import os

import pyshark
from pyshark.capture.capture import TSharkCrashException


class AsyncFileCapture(pyshark.FileCapture):
    async def async_load_packets(self, packet_count=None):
        """
        Reads the packets from the source (cap, interface, etc.) and adds it to the internal list.
        """
        await self.packets_from_tshark(self._packets.append, packet_count=packet_count)
        self.loaded = True


class UuSniffer:
    READING_CHUNK = 20

    def __init__(self, uu_cap, parser):
        self._cap_index = 0
        self._run = True
        self._uu_cap = uu_cap
        self._parser = parser

    async def start(self):
        """
        Start tracking the Uu capture file for new packets.
        """
        while not os.path.exists(self._uu_cap):
            await asyncio.sleep(0)

        # We use our own version of FileCapture since the original is not really async.
        cap = AsyncFileCapture(self._uu_cap)
        while self._run:
            # TShark might crash because the last packet might not be fully written, it will be read on the next reload.
            try:
                await self._reload_cap(cap)
                self._publish_new_packets(cap)
                self._cap_index = len(cap)
            except TSharkCrashException:
                continue

    def stop(self):
        """
        Stop tracking.
        """
        self._run = False

    async def _reload_cap(self, cap):
        cap.clear()
        # Read packets in chunks since PCAP file end might be corrupted.
        await cap.async_load_packets(packet_count=self._cap_index + self.READING_CHUNK)

    def _publish_new_packets(self, cap):
        for i, packet in enumerate(cap):
            if i < self._cap_index:
                # Packets already read.
                continue
            self._parser.from_packet(packet)
