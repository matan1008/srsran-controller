import asyncio
from abc import abstractmethod, ABC
from asyncio.queues import Queue
from datetime import datetime
from enum import Enum, auto
from logging import getLogger
from uuid import uuid4


class ScriptStatus(Enum):
    PENDING = auto()
    STARTED = auto()
    STOPPED = auto()
    ERROR = auto()
    COMPLETED = auto()


class AbstractScript(ABC):
    def __init__(self):
        self._logger = getLogger('srsran_controller')
        self.imsi = None
        self.mission = None
        self.executor = None
        self.stopped = False
        self.id = str(uuid4())
        self.logs = []
        self.start_time = datetime.now()
        self.stop_time = None
        self._status = ScriptStatus.PENDING
        self.uu_queue = Queue()
        self.main_task = None

    @classmethod
    def get_name(cls):
        return getattr(cls, 'NAME', str(cls.__name__))

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: ScriptStatus):
        self._status = value
        self._logger.info(f'Script id {self.id} - status change: {value}')
        self.executor.handle_script_status(self)

    async def stop(self) -> None:
        """
        Stop the script.
        """
        if self.stopped:
            return
        self.stopped = True
        self.main_task.cancel()

    async def start(self, imsi: str, mission, executor) -> None:
        """
        :param imsi: UE's IMSI.
        :param srsran_controller.mission.mission.Mission mission: Current mission.
        :param srsran_controller.scripts.executor.ScriptsExecutor executor: Scripts executor.
        """
        self.imsi = imsi
        self.mission = mission
        self.executor = executor
        self.main_task = asyncio.create_task(self._wrapped_run())

    def log(self, log: str) -> None:
        """
        Write log line from the current script.
        :param log: Data to write.
        """
        self._logger.info(f'Script id {self.id} - log: {log}')
        time = datetime.now()
        self.logs.append((time, log))
        self.executor.handle_script_log(self, time, log)

    @abstractmethod
    async def run(self) -> None:
        """
        Script's main logic.
        """

    def handle_new_uu_packet(self, enb_ip: str, rnti: int, packet) -> None:
        """
        Handle arrival of a new packet.
        :param enb_ip: IP of enb.
        :param rnti: C-RNTI of the packet.
        :param packet: Parsed packet object.
        """
        try:
            if self.mission.channel_tracker.get_channel(enb_ip, rnti).imsi != self.imsi:
                return
        except KeyError:
            self._logger.error(f'Script {self.id} failed to find channel ({enb_ip}, {rnti})')
            return
        self.uu_queue.put_nowait(packet)

    async def wait_for_parsed_packet(self, validator):
        """
        Wait for a specific packet.
        :param validator: Callback function to match the desired packet.
        :return: Packet's object.
        """
        while True:
            packet = await self.uu_queue.get()
            try:
                if validator(packet):
                    return packet
            except (KeyError, AttributeError):
                pass

    async def _wrapped_run(self):
        try:
            self.status = ScriptStatus.STARTED
            await self.run()
        except asyncio.CancelledError:
            self.status = ScriptStatus.STOPPED
        except Exception as e:
            self.log(str(e))
            self.status = ScriptStatus.ERROR
        else:
            self.status = ScriptStatus.COMPLETED
        self.stopped = True
        self.stop_time = datetime.now()
