import docker

from srslte_controller.configuration import config
from srslte_controller.mission.entity import Entity


class Enb(Entity):
    CONTAINER_NAME = 'enb'
    ENB_CONF_CONTAINER_PATH = '/mnt/enb.conf'
    ENB_SIBS_CONF_CONTAINER_PATH = '/mnt/enb_sibs.conf'
    ENB_DRBS_CONF_CONTAINER_PATH = '/mnt/enb_drbs.conf'
    ENB_RR_CONF_CONTAINER_PATH = '/mnt/enb_rr.conf'
    ENB_COMMAND = f'srsenb {ENB_CONF_CONTAINER_PATH}'

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
        client = docker.from_env()
        volumes = {
            configuration_path: {'bind': Enb.ENB_CONF_CONTAINER_PATH, 'mode': 'ro'},
            sibs_path: {'bind': Enb.ENB_SIBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            drbs_path: {'bind': Enb.ENB_DRBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            rr_path: {'bind': Enb.ENB_RR_CONF_CONTAINER_PATH, 'mode': 'ro'},
        }
        container = client.containers.create(
            config.enb_docker_image, Enb.ENB_COMMAND, detach=True, volumes=volumes, auto_remove=True,
            name=Enb.CONTAINER_NAME, network_mode='none'
        )
        enb = Enb(container)
        enb._connect_to_network(network_id, ip)
        container.start()
        enb._wait_for_ip()
        return enb
