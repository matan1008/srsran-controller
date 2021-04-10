import asyncio
import os
import subprocess

import pyshark


class AsyncFileCapture(pyshark.FileCapture):
    async def async_load_packets(self, packet_count=None):
        """
        Reads the packets from the source (cap, interface, etc.) and adds it to the internal list.
        """
        await self.packets_from_tshark(self._packets.append, packet_count=packet_count)
        self.loaded = True


class UuSniffer:
    FIXED_CAP_FILE = '/tmp/fixed_enb.pcap'

    def __init__(self, uu_cap, parser):
        self._cap_index = 0
        self._run = True
        self._uu_cap = uu_cap
        self._parser = parser

    async def start(self):
        """
        Start tracking the Uu capture file for new packets.
        """
        while not os.path.exists(self._uu_cap) or not os.stat(self._uu_cap).st_size:
            await asyncio.sleep(0)

        # We use our own version of FileCapture since the original is not really async.
        cap = AsyncFileCapture(self.FIXED_CAP_FILE)
        while self._run:
            await self._fix_pcap()
            await self._reload_cap(cap)
            self._publish_new_packets(cap)
            self._cap_index = len(cap)

    def stop(self):
        """
        Stop tracking.
        """
        self._run = False

    @staticmethod
    async def _reload_cap(cap):
        cap.clear()
        await cap.async_load_packets()

    async def _fix_pcap(self):
        await asyncio.create_subprocess_exec(
            'pcapfix', self._uu_cap, '-o', self.FIXED_CAP_FILE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def _publish_new_packets(self, cap):
        for i, packet in enumerate(cap):
            if i < self._cap_index:
                # Packets already read.
                continue
            self._parser.from_packet(packet)
