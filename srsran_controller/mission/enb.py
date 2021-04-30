import os
import pathlib

import docker

from srsran_controller.configuration import config
from srsran_controller.mission.entity import Entity


class Enb(Entity):
    CONTAINER_NAME = 'enb'
    CONF_CONTAINER_PATH = '/mnt/enb.conf'
    SIBS_CONF_CONTAINER_PATH = '/mnt/enb_sibs.conf'
    DRBS_CONF_CONTAINER_PATH = '/mnt/enb_drbs.conf'
    RR_CONF_CONTAINER_PATH = '/mnt/enb_rr.conf'
    CAP_CONTAINER_PATH = '/tmp/enb.pcap'
    COMMAND = f'srsenb {CONF_CONTAINER_PATH}'
    LOG_CONTAINER_PATH = '/tmp/enb.log'

    @staticmethod
    def create(configuration_path: str, sibs_path: str, drbs_path: str, rr_path: str, network_id: str, ip: str):
        """
        Create a SrsENB instance.
        :param configuration_path: SrsENB configuration path.
        :param sibs_path: Sibs configuration path.
        :param drbs_path: DRBs configuration path.
        :param rr_path: RR configuration path.
        :param network_id: Docker network to attach to.
        :param ip: Container IP inside the network.
        """
        # The previous CAP file is irrelevant.
        pathlib.Path(config.current_enb_cap).unlink(missing_ok=True)
        client = docker.from_env()
        volumes = {
            configuration_path: {'bind': Enb.CONF_CONTAINER_PATH, 'mode': 'ro'},
            sibs_path: {'bind': Enb.SIBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            drbs_path: {'bind': Enb.DRBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            rr_path: {'bind': Enb.RR_CONF_CONTAINER_PATH, 'mode': 'ro'},
            os.path.dirname(config.current_enb_cap): {'bind': os.path.dirname(Enb.CAP_CONTAINER_PATH), 'mode': 'rw'},
        }
        container = client.containers.create(
            config.enb_docker_image, Enb.COMMAND, detach=True, volumes=volumes, auto_remove=True,
            name=Enb.CONTAINER_NAME, network_mode='none'
        )
        enb = Enb(container)
        enb._connect_to_network(network_id, ip)
        container.start()
        enb._wait_for_ip()
        return enb
