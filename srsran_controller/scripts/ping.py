import asyncio

from srsran_controller.scripts.abstract import AbstractScript


class Ping(AbstractScript):
    STOP_COMMAND = b'\x03'
    PING_COMMAND = 'ping {}'

    async def run(self) -> None:
        ip = self.mission.channel_tracker.imsi_to_ip(self.imsi)
        _, sock = self.mission.epc.container.exec_run(Ping.PING_COMMAND.format(ip), stdin=True, socket=True, tty=True)
        reader, writer = await asyncio.open_connection(sock=sock._sock)
        try:
            async for log in reader:
                self.log(log.decode().strip())
        except asyncio.CancelledError:
            pass
        # Send ^C to the ping process.
        writer.write(self.STOP_COMMAND)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
