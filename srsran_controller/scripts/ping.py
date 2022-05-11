import asyncio

from srsran_controller.scripts.abstract import AbstractScript


class Ping(AbstractScript):
    STOP_COMMAND = b'\x03'
    PING_COMMAND = 'ping {}'

    def __init__(self, imsi: str, mission, manager, ip: str, reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        super().__init__(imsi, mission, manager)
        self.ip = ip
        self._reader = reader
        self._writer = writer
        self._read_logs_task = asyncio.create_task(self._read_logs())

    @staticmethod
    async def create(imsi: str, mission, manager):
        """
        Factory method for Ping objects.
        :param imsi: UE's IMSI.
        :param mission: Launched mission to run ping on.
        :param manager: Scripts manager.
        :return: Initialized and running ping object.
        :rtype: Ping
        """
        ip = mission.channel_tracker.imsi_to_ip(imsi)
        _, sock = mission.epc.container.exec_run(Ping.PING_COMMAND.format(ip), stdin=True, socket=True, tty=True)
        return Ping(imsi, mission, manager, ip, *await asyncio.open_connection(sock=sock._sock))

    async def clean(self):
        """
        Stop pinging the UE.
        """
        # Prevent reading a ^C.
        self._read_logs_task.cancel()
        await self._read_logs_task
        # Send ^C to the ping process.
        self._writer.write(self.STOP_COMMAND)
        await self._writer.drain()
        self._writer.close()
        await self._writer.wait_closed()

    async def _read_logs(self):
        try:
            async for log in self._reader:
                self.log(log.decode().strip())
        except asyncio.CancelledError:
            pass
