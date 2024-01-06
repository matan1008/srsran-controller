import asyncio
import socket
from contextlib import closing, suppress

import psutil
from pyshark import LiveCapture


class AioClosingLiveCapture(LiveCapture):
    async def close_async(self):
        for process in self._running_processes.copy():
            with suppress(psutil.NoSuchProcess):
                for child in psutil.Process(process.pid).children():
                    child.kill()
            await self._cleanup_subprocess(process)
        self._running_processes.clear()

        # Wait for all stderr handling to finish
        await asyncio.gather(*self._stderr_handling_tasks)


class UuSniffer:
    MAC_LTE_PORT = 5847

    def __init__(self, interface, addr, port=MAC_LTE_PORT):
        self._interface = interface
        self._addr = addr
        self._port = port

    async def start(self, use_json: bool = False):
        """
        Start tracking the Uu interface for new packets.
        :rtype: types.AsyncGeneratorType
        """
        # The socket is required in order to prevent ICMP destination port unreachable from being sent.
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind((self._addr, self._port))
            packet_queue = asyncio.Queue()
            async with AioClosingLiveCapture(bpf_filter=f'udp port {self._port}', interface=self._interface,
                                             use_json=use_json, eventloop=asyncio.get_event_loop()) as cap:
                cap_task = asyncio.create_task(cap.packets_from_tshark(packet_queue.put_nowait))
                try:
                    while True:
                        yield await packet_queue.get()
                except asyncio.CancelledError:
                    cap_task.cancel()
