from abc import abstractmethod, ABC

from datetime import datetime
from enum import Enum
from logging import getLogger
from uuid import uuid4


class ScriptStatus(Enum):
    STARTED = 0
    STOPPED = 1


class AbstractScript(ABC):
    def __init__(self, imsi: str, mission, manager):
        """
        :param srsran_controller.mission.mission.Mission mission: Current mission.
        :param srsran_controller.scripts.manager.ScriptsManager manager: Scripts manager.
        """
        self._logger = getLogger('srsran_controller')
        self.imsi = imsi
        self.mission = mission
        self.manager = manager
        self.stopped = False
        self.id = str(uuid4())
        self.logs = []
        self.start_time = datetime.now()
        self.stop_time = None
        self.status = ScriptStatus.STARTED

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: ScriptStatus):
        self._status = value
        self._logger.info(f'Script id {self.id} - status change: {value}')
        self.manager.handle_script_status(self)

    async def stop(self) -> None:
        """
        Stop the script.
        """
        if self.stopped:
            return
        self.stopped = True
        await self.clean()
        self.stop_time = datetime.now()
        self.status = ScriptStatus.STOPPED

    def log(self, log: str) -> None:
        """
        Write log line from the current script.
        :param log: Data to write.
        """
        self._logger.info(f'Script id {self.id} - log: {log}')
        time = datetime.now()
        self.logs.append((time, log))
        self.manager.handle_script_log(self, time, log)

    @abstractmethod
    async def clean(self) -> None:
        """
        Script specific cleaning operation.
        """
        pass
