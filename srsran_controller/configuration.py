import json
from dataclasses import dataclass, fields


@dataclass
class Configuration:
    """
    Global scoped configuration.
    """
    missions_configurations_folder: str
    current_epc_configuration: str
    current_enb_configuration: str
    current_enb_sibs_configuration: str
    current_enb_drbs_configuration: str
    current_enb_rr_configuration: str
    users_db: str
    epc_docker_image: str = 'srsran-controller-docker:latest'
    enb_docker_image: str = 'srsran-controller-docker:latest'

    def reload(self, path: str):
        """
        Update configuration values from a json file.
        :param path: Path to a json configuration.
        """
        with open(path, 'r') as fd:
            data = json.load(fd)
        for field in fields(self):
            setattr(self, field.name, data.get(field.name, getattr(self, field.name)))


# Since it contains paths, intentionally create it with invalid values so it must be reloaded before using it.

config = Configuration(
    missions_configurations_folder='',
    current_epc_configuration='',
    current_enb_configuration='',
    current_enb_sibs_configuration='',
    current_enb_drbs_configuration='',
    current_enb_rr_configuration='',
    users_db='',
)
