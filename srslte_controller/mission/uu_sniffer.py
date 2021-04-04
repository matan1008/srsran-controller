import asyncio
import os

import pyshark
from pyshark.capture.capture import TSharkCrashException


class AsyncFileCapture(pyshark.FileCapture):
    async def async_load_packets(self):
        """
        Reads the packets from the source (cap, interface, etc.) and adds it to the internal list.
        """
        await self.packets_from_tshark(self._packets.append)
        self.loaded = True


class UuSniffer:
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
        cap = AsyncFileCapture(self._uu_cap, display_filter='!lte-rrc.BCCH_DL_SCH_Message_element')
        while self._run:
            await self._reload_cap(cap)
            self._publish_new_packets(cap)
            self._cap_index = len(cap)

    def stop(self):
        """
        Stop tracking.
        """
        self._run = False

    async def _reload_cap(self, cap):
        # TShark might crash because the last packet might not be fully written, it will be read on the next reload.
        while self._run:
            try:
                cap.clear()
                await cap.async_load_packets()
            except TSharkCrashException:
                continue
            else:
                break

    def _publish_new_packets(self, cap):
        for i, packet in enumerate(cap):
            if i < self._cap_index:
                continue
            self._parser.from_packet(packet)
