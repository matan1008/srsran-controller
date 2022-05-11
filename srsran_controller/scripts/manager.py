import asyncio
from datetime import datetime
from logging import getLogger


class ScriptsManager:
    def __init__(self):
        self.scripts = []
        self.logger = getLogger('srsran_controller')
        self.script_status_callback = lambda script: None
        self.script_log_callback = lambda script, time, log: None

    async def start_script(self, factory, imsi: str, mission):
        """
        Start a script.
        :param factory: Coroutine to create script with.
        :param imsi: Script subject's IMSI.
        :param mission: Current mission.
        :return: Created script.
        :rtype: srsran_controller.scripts.abstract.AbstractScript
        """
        script = await factory(imsi, mission, self)
        self.logger.info(f'Starting script id {script.id} on {imsi}')
        self.scripts.append(script)
        return script

    async def stop_script(self, id_: str) -> None:
        """
        Stop a running script.
        :param id_: Script ID.
        """
        self.logger.info(f'Stopping script id {id_}')
        for script in self.scripts:
            if not script.stopped and script.id == id_:
                await script.stop()

    async def stop_all(self):
        """
        Stop all running scripts.
        """
        await asyncio.gather(*[script.stop() for script in self.scripts if not script.stopped])

    def handle_script_status(self, script):
        """
        Handle script status changes.
        :param script: Script on which the change happened.
        """
        self.script_status_callback(script)

    def handle_script_log(self, script, time: datetime, log: str):
        """
        Handle a script log line.
        :param script: Script which required the logging.
        :param time: Log's time.
        :param log: Log's data.
        """
        self.script_log_callback(script, time, log)
