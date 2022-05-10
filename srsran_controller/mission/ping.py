import asyncio
from datetime import datetime
from enum import Enum
from uuid import uuid4


class PingStatus(Enum):
    STARTED = 0
    STOPPED = 1


class Ping:
    STOP_COMMAND = b'\x03'
    PING_COMMAND = 'ping {}'

    def __init__(self, ip: str, imsi: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, status_callback,
                 log_callback):
        self._reader = reader
        self._writer = writer
        self._status_callback = status_callback
        self._log_callback = log_callback
        self.ip = ip
        self.imsi = imsi
        self.status = PingStatus.STARTED
        self.stopped = False
        self.id = str(uuid4())
        self.logs = []
        self.start_time = datetime.now()
        self.stop_time = None
        self._read_logs_task = asyncio.create_task(self._read_logs())

    @staticmethod
    async def create(epc, ip: str, imsi: str, status_callback, log_callback):
        """
        Factory method for Ping objects.
        :param srsran_controller.mission.epc.Epc epc: Current EPC.
        :param ip: IP address pf the UE.
        :param imsi: UE's IMSI.
        :param status_callback: Callback function to be called on state changes.
        :param log_callback: Callback function to be called when new log is fetched.
        :return: Initialized and running ping object.
        :rtype: Ping
        """
        _, sock = epc.container.exec_run(Ping.PING_COMMAND.format(ip), stdin=True, socket=True, tty=True)
        ping = Ping(ip, imsi, *await asyncio.open_connection(sock=sock._sock), status_callback, log_callback)
        status_callback(ping)
        return ping

    async def stop(self) -> None:
        """
        Stop pinging the UE.
        """
        if self.stopped:
            return
        # Prevent reading a ^C.
        self._read_logs_task.cancel()
        await self._read_logs_task
        # Send ^C to the ping process.
        self._writer.write(self.STOP_COMMAND)
        await self._writer.drain()
        self._writer.close()
        await self._writer.wait_closed()
        self.stop_time = datetime.now()
        self.stopped = True
        self.status = PingStatus.STOPPED
        self._status_callback(self)

    async def _read_logs(self):
        try:
            async for log in self._reader:
                log = log.decode()
                self.logs.append((datetime.now(), log))
                self._log_callback(self, datetime.now(), log)
        except asyncio.CancelledError:
            pass
