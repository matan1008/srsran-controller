import json
from dataclasses import dataclass, fields


@dataclass
class Configuration:
    missions_configurations_folder: str
    current_epc_configuration: str
    current_enb_configuration: str
    users_db: str
    epc_docker_image: str = 'srslte-controller-docker:latest'
    enb_docker_image: str = 'srslte-controller-docker:latest'

    def reload(self, path):
        with open(path, 'r') as fd:
            data = json.load(fd)
        for field in fields(self):
            setattr(self, field.name, data.get(field.name, getattr(self, field.name)))


# Since it contains paths, intentionally create it with invalid values so it must be reloaded before using it.

config = Configuration('', '', '', '')
