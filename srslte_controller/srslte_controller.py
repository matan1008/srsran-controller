import srslte_controller.exceptions as exceptions
from srslte_controller.configuration import config
from srslte_controller.configurations_manager import ConfigurationsManager
from srslte_controller.mission.mission import Mission
from srslte_controller.mission.mission_factory import MissionFactory


class SrslteController:

    def __init__(self, configuration_path):
        config.reload(configuration_path)
        self.configurations = ConfigurationsManager(config.missions_configurations_folder)
        self._current_mission = None

    @property
    def current_mission(self) -> Mission:
        return self._current_mission

    def is_mission_up(self):
        return self.current_mission is not None

    def launch_mission(self, mission_configuration_id):
        if self.is_mission_up():
            raise exceptions.MissionAlreadyRunningError()

        self._current_mission = MissionFactory.create(self.configurations.get_mission(mission_configuration_id))

    def stop_mission(self):
        self.current_mission.stop()
        self._current_mission = None
