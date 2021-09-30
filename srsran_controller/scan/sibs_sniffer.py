import docker

from srsran_controller.common.docker.entity import Entity
from srsran_controller.configuration import config
from srsran_controller.srsran_configurations.ue import *


class SibsScanner(Entity):
    CONF_CONTAINER_PATH = '/mnt/ue.conf'
    CONTAINER_NAME = 'sibs-scanner'
    COMMAND = f'srsue {CONF_CONTAINER_PATH}'
    CLIENT_IP = '127.0.0.1'

    @staticmethod
    def create(configuration_path: str):
        """
        Create a SibsScanner instance.
        :param configuration_path: SrsUe configuration path.
        :return: SibsScanner object.
        :rtype: SibsScanner
        """
        client = docker.from_env()
        volumes = {configuration_path: {'bind': SibsScanner.CONF_CONTAINER_PATH, 'mode': 'ro'}}
        container = client.containers.create(
            config.scanner_docker_image, SibsScanner.COMMAND, auto_remove=True,
            name=SibsScanner.CONTAINER_NAME, network_mode='host', privileged=True, volumes=volumes
        )
        scanner = SibsScanner(container)
        return scanner


def _build_ue_configuration(earfcn, cell_id, client_ip):
    return SrsUeConfiguration(
        rat_eutra=SrsUeRatEutraConfiguration(dl_earfcn=earfcn),
        pcap=SrsUePcapConfiguration(mac_net_enable=True, client_ip=client_ip),
        usim=SrsUeUsimConfiguration(  # We are not going to authenticate anyway
            opc='0' * 32,
            k='0' * 32,
            imsi='1' * 15,
            imei='3' * 15,
        ),
        phy=SrsUePhyConfiguration(force_N_id_2=cell_id % 3)
    )


def create_sibs_sniffer(earfcn, cell_id) -> SibsScanner:
    """
    Start a SibsSniffer
    :param earfcn: EARFCN of cell to sniff.
    :param cell_id: Cell Id of cell to sniff.
    :return: Sniffing sibs scanner object.
    """
    with open(config.current_ue_configuration, 'w') as fd:
        _build_ue_configuration(earfcn, cell_id, SibsScanner.CLIENT_IP).write(fd)
    sibs_scanner = SibsScanner.create(config.current_ue_configuration)
    sibs_scanner.start()
    return sibs_scanner
