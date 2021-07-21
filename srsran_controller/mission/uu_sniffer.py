import asyncio
import socket
from contextlib import closing

import pyshark


class AsyncLiveCapture(pyshark.LiveCapture):
    async def sniff_continuously(self, packet_count=None):
        tshark_process = await self._get_tshark_process()
        psml_structure, data = await self._get_psml_struct(tshark_process.stdout)
        packets_captured = 0

        data = b''
        try:
            while True:
                try:
                    packet, data = await self._get_packet_from_stream(tshark_process.stdout, data,
                                                                      psml_structure=psml_structure,
                                                                      got_first_packet=packets_captured > 0)
                except EOFError:
                    self._log.debug('EOF reached (sync)')
                    self._eof_reached = True
                    break

                if packet:
                    packets_captured += 1
                    yield packet
                if packet_count and packets_captured >= packet_count:
                    break
        finally:
            if tshark_process in self._running_processes:
                await self._cleanup_subprocess(tshark_process)


class UuSniffer:
    MAC_LTE_PORT = 5847

    def __init__(self, parser, interface, addr, port=MAC_LTE_PORT):
        self._parser = parser
        self._interface = interface
        self._addr = addr
        self._port = port

    async def start(self):
        """
        Start tracking the Uu interface for new packets.
        """
        # The socket is required in order to prevent ICMP destination port unreachable from being sent.
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind((self._addr, self._port))
            try:
                async with AsyncLiveCapture(bpf_filter=f'udp port {self._port}', interface=self._interface,
                                            eventloop=asyncio.get_event_loop()) as cap:
                    gen = cap.sniff_continuously()
                    while True:
                        packet = await gen.__anext__()
                        self._parser.from_packet(packet)
            except asyncio.CancelledError:
                pass
