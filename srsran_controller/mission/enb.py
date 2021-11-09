import docker

from srsran_controller.configuration import config
from srsran_controller.common.docker.entity import Entity


class Enb(Entity):
    CONTAINER_NAME = 'enb'
    CONF_CONTAINER_PATH = '/mnt/enb.conf'
    SIBS_CONF_CONTAINER_PATH = '/mnt/enb_sibs.conf'
    RBS_CONF_CONTAINER_PATH = '/mnt/enb_rbs.conf'
    RR_CONF_CONTAINER_PATH = '/mnt/enb_rr.conf'
    COMMAND = f'srsenb {CONF_CONTAINER_PATH}'
    LOG_CONTAINER_PATH = '/tmp/enb.log'

    @staticmethod
    def create(configuration_path: str, sibs_path: str, rbs_path: str, rr_path: str):
        """
        Create a SrsENB instance.
        :param configuration_path: SrsENB configuration path.
        :param sibs_path: Sibs configuration path.
        :param rbs_path: RBs configuration path.
        :param rr_path: RR configuration path.
        """
        client = docker.from_env()
        volumes = {
            configuration_path: {'bind': Enb.CONF_CONTAINER_PATH, 'mode': 'ro'},
            sibs_path: {'bind': Enb.SIBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            rbs_path: {'bind': Enb.RBS_CONF_CONTAINER_PATH, 'mode': 'ro'},
            rr_path: {'bind': Enb.RR_CONF_CONTAINER_PATH, 'mode': 'ro'},
        }
        container = client.containers.create(
            config.enb_docker_image, Enb.COMMAND, detach=True, volumes=volumes, auto_remove=True,
            name=Enb.CONTAINER_NAME, network_mode='none', privileged=True
        )
        enb = Enb(container)
        enb._disconnect('none')
        return enb
