import json
from dataclasses import dataclass, fields
from pathlib import Path

from srsran_controller.common.utils import LazyList


@dataclass
class Configuration:
    """
    Global scoped configuration.
    """
    missions_configurations_folder: str
    scripts_folder: str
    current_configurations_folder: str
    users_db: str
    scan_results: str
    products_folder: str
    epc_docker_image: str = 'srsran-controller-docker:latest'
    enb_docker_image: str = 'srsran-controller-docker:latest'
    scanner_docker_image: str = 'srsran-controller-docker:latest'
    sudo_password: str = ''  # Never save it in a json, required for run time only.

    @property
    def current_epc_configuration(self) -> Path:
        return Path(self.current_configurations_folder) / 'epc.conf'

    @property
    def current_ue_configuration(self) -> Path:
        return Path(self.current_configurations_folder) / 'ue.conf'

    @property
    def current_enb_configuration(self) -> list[Path]:
        return LazyList(lambda i: Path(self.current_configurations_folder) / f'enb{i}.conf')

    @property
    def current_enb_sibs_configuration(self) -> list[Path]:
        return LazyList(lambda i: Path(self.current_configurations_folder) / f'enb_sibs{i}.conf')

    @property
    def current_enb_rbs_configuration(self) -> list[Path]:
        return LazyList(lambda i: Path(self.current_configurations_folder) / f'enb_rbs{i}.conf')

    @property
    def current_enb_rr_configuration(self) -> list[Path]:
        return LazyList(lambda i: Path(self.current_configurations_folder) / f'enb_rr{i}.conf')

    def reload(self, path: str):
        """
        Update configuration values from a json file.
        :param path: Path to a json configuration.
        """
        with open(path, 'r') as fd:
            data = json.load(fd)
        for field in fields(self):
            setattr(self, field.name, data.get(field.name, getattr(self, field.name)))


# Since it contains paths, intentionally create it with invalid values, so it must be reloaded before using it.

config = Configuration(
    missions_configurations_folder='',
    scripts_folder='',
    current_configurations_folder='',
    users_db='',
    scan_results='',
    products_folder='',
)
