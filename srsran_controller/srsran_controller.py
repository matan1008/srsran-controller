import pathlib

import srsran_controller.exceptions as exceptions
from srsran_controller.configuration import config
from srsran_controller.configurations_manager import ConfigurationsManager
from srsran_controller.mission.mission import Mission
from srsran_controller.mission_factory.mission import create as create_mission


class SrsranController:

    def __init__(self, configuration_path):
        config.reload(configuration_path)
        self.configurations = ConfigurationsManager(config.missions_configurations_folder)
        pathlib.Path(config.missions_configurations_folder).mkdir(parents=True, exist_ok=True)
        self._current_mission = None

    @property
    def current_mission(self) -> Mission:
        return self._current_mission

    def is_mission_up(self) -> bool:
        """
        :return: True if a mission is running, False otherwise.
        """
        return self.current_mission is not None

    async def launch_mission(self, mission_configuration_id: str) -> Mission:
        """
        Launch a mission.
        :param mission_configuration_id: Mission configuration id.
        :return: Launched mission object.
        :raises exceptions.MissionAlreadyRunningError: When trying to launch a mission while another mission is running.
        """
        if self.is_mission_up():
            raise exceptions.MissionAlreadyRunningError()

        self._current_mission = await create_mission(self.configurations.get_mission(mission_configuration_id))
        return self._current_mission

    async def stop_mission(self):
        """
        Stop the running mission.
        """
        await self.current_mission.stop()
        self._current_mission = None
