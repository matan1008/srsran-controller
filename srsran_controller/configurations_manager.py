import json
from dataclasses import asdict
from pathlib import Path

from srsran_controller.exceptions import MissionIdNotFoundError
from srsran_controller.mission.mission_configuration import MissionConfiguration


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

    def list_missions(self):
        missions = []
        for f, data in self._iter_missions():
            try:
                missions.append(MissionConfiguration.from_dict(data))
            except TypeError:
                print(f'Could not load mission {f.name}')
        return missions

    @property
    def _missions_path(self) -> Path:
        return Path(self._missions_configurations_folder)

    def _iter_missions(self):
        for f in filter(lambda p: p.is_file(), self._missions_path.iterdir()):
            try:
                with open(f, 'r') as fd:
                    yield f, json.load(fd)
            except json.JSONDecodeError:
                pass

    def _on_mission_configuration(self, configuration_id, operation):
        for f, data in self._iter_missions():
            if data['id'] == configuration_id:
                return operation(f, data)
        raise MissionIdNotFoundError()
