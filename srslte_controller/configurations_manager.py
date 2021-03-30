import json
import pathlib
from dataclasses import asdict

from srslte_controller.exceptions import MissionIdNotFoundError
from srslte_controller.mission.mission_configuration import MissionConfiguration


class ConfigurationsManager:
    def __init__(self, missions_configurations_folder: str):
        self._missions_configurations_folder = missions_configurations_folder

    def create_mission(self):
        configuration = MissionConfiguration()
        with open(self._missions_path.joinpath(configuration.id), 'w') as fd:
            json.dump(asdict(configuration), fd, indent=4)
        return configuration

    def get_mission(self, mission_configuration_id):
        return self._on_mission_configuration(
            mission_configuration_id, lambda f, data: MissionConfiguration.from_dict(data)
        )

    def update_mission(self, configuration):
        def _update_callback(path, _data):
            with open(path, 'w') as fd:
                json.dump(asdict(configuration), fd, indent=4)

        return self._on_mission_configuration(configuration.id, _update_callback)

    def delete_mission(self, mission_configuration_id):
        self._on_mission_configuration(mission_configuration_id, lambda f, data: f.unlink())

    @property
    def _missions_path(self):
        return pathlib.Path(self._missions_configurations_folder)

    def _on_mission_configuration(self, configuration_id, operation):
        for f in filter(lambda p: p.is_file(), self._missions_path.iterdir()):
            try:
                with open(f, 'r') as fd:
                    data = json.load(fd)
                if data['id'] == configuration_id:
                    return operation(f, data)
            except json.JSONDecodeError:
                pass
        raise MissionIdNotFoundError()
