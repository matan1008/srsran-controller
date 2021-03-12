import json

missions_configurations_folder: str
current_epc_configuration: str
current_enb_configuration: str
users_db: str
epc_docker_image: str = 'srslte-controller-docker:latest'
enb_docker_image: str = 'srslte-controller-docker:latest'


def reload(path):
    global missions_configurations_folder
    global current_epc_configuration
    global current_enb_configuration
    global users_db

    with open(path, 'r') as fd:
        data = json.load(fd)

    missions_configurations_folder = data['missions_configurations_folder']
    current_epc_configuration = data['current_epc_configuration']
    current_enb_configuration = data['current_enb_configuration']
    users_db = data['users_db']
