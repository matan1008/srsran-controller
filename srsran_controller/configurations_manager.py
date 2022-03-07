import json
from dataclasses import asdict
from logging import Logger, getLogger
from pathlib import Path

from srsran_controller.exceptions import MissionIdNotFoundError
from srsran_controller.mission.mission_configuration import MissionConfiguration


class ConfigurationsManager:
    def __init__(self, missions_configurations_folder: str, logger: Logger = getLogger('srsran_controller')):
        """
        :param missions_configurations_folder: Directory to save all mission in.
        :param logger: Logger for the configuration manager.
        """
        self.logger = logger
        self._missions_configurations_folder = missions_configurations_folder

    def create_mission(self) -> MissionConfiguration:
        """
        Create a new mission configuration.
        :return: Newly create mission.
        """
        configuration = MissionConfiguration()
        with open(self._missions_path.joinpath(configuration.id), 'w') as fd:
            json.dump(asdict(configuration), fd, indent=4)
        self.logger.info(f'Mission {configuration.id} created')
        return configuration

    def get_mission(self, mission_configuration_id: str) -> MissionConfiguration:
        """
        Find mission configuration by its id.
        :param mission_configuration_id: Requested mission id.
        :return: Mission configuration.
        """
        return self._on_mission_configuration(
            mission_configuration_id, lambda f, data: MissionConfiguration.from_dict(data)
        )

    def update_mission(self, configuration: MissionConfiguration) -> None:
        """
        Update mission configuration.
        :param configuration: New configuration for a mission.
        """

        def _update_callback(path, _data):
            with open(path, 'w') as fd:
                self.logger.debug(f'Updating mission {_data} to {asdict(configuration)}')
                json.dump(asdict(configuration), fd, indent=4)
                self.logger.info(f'Mission {configuration.id} updated')

        self._on_mission_configuration(configuration.id, _update_callback)

    def delete_mission(self, mission_configuration_id: str) -> None:
        """
        Delete a mission configuration.
        :param mission_configuration_id: ID of mission to delete.
        """
        self._on_mission_configuration(mission_configuration_id, lambda f, data: f.unlink())
        self.logger.info(f'Mission {mission_configuration_id} deleted')

    def list_missions(self) -> list[MissionConfiguration]:
        """
        List all missions in missions configurations folder.
        :return: List of mission configurations.
        """
        missions = []
        for f, data in self._iter_missions():
            try:
                missions.append(MissionConfiguration.from_dict(data))
            except TypeError:
                self.logger.warning(f'Could not load mission {f.name}', exc_info=True)
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
                self.logger.warning(f'Could not decode {f.name} in missions folder')

    def _on_mission_configuration(self, configuration_id: str, operation):
        for f, data in self._iter_missions():
            if data['id'] == configuration_id:
                return operation(f, data)
        raise MissionIdNotFoundError()
