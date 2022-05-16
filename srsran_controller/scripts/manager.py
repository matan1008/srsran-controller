import asyncio
from datetime import datetime
from logging import getLogger

CRNTI_TYPE = 3


class ScriptsManager:
    def __init__(self):
        self.scripts = []
        self.logger = getLogger('srsran_controller')
        self.script_status_callback = lambda script: None
        self.script_log_callback = lambda script, time, log: None

    async def start_script(self, script, imsi: str, mission):
        """
        Start a script.
        :param srsran_controller.scripts.abstract.AbstractScript script: Script to start.
        :param imsi: Script subject's IMSI.
        :param mission: Current mission.
        """
        self.scripts.append(script)
        self.logger.info(f'Starting script id {script.id} on {imsi}')
        await script.start(imsi, mission, self)

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

    def handle_new_uu_packet(self, pkt):
        """
        Handle arrival of a new UU packet.
        """
        mac_layer = getattr(pkt, 'mac-lte', None)
        if mac_layer is None or int(mac_layer.rnti_type) != CRNTI_TYPE:
            return
        for script in filter(lambda s: not s.stopped, self.scripts):
            script.handle_new_uu_packet(int(mac_layer.rnti), pkt)
