import asyncio
import socket
from contextlib import closing

from pyshark import LiveCapture


class UuSniffer:
    MAC_LTE_PORT = 5847

    def __init__(self, interface, addr, port=MAC_LTE_PORT):
        self._interface = interface
        self._addr = addr
        self._port = port

    async def start(self, use_ek: bool = False):
        """
        Start tracking the Uu interface for new packets.
        :rtype: types.AsyncGeneratorType
        """
        # The socket is required in order to prevent ICMP destination port unreachable from being sent.
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind((self._addr, self._port))
            packet_queue = asyncio.Queue()
            async with LiveCapture(bpf_filter=f'udp port {self._port}', interface=self._interface, use_ek=use_ek,
                                   eventloop=asyncio.get_event_loop()) as cap:
                cap_task = asyncio.create_task(cap.packets_from_tshark(packet_queue.put_nowait))
                try:
                    while True:
                        yield await packet_queue.get()
                except asyncio.CancelledError:
                    cap_task.cancel()
