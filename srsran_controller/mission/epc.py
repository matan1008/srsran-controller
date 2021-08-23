import docker

from srsran_controller.configuration import config
from srsran_controller.mission.entity import Entity


class Epc(Entity):
    CONTAINER_NAME = 'epc'
    CONF_CONTAINER_PATH = '/mnt/epc.conf'
    HSS_CONFIGURATION_PATH = '/mnt/user_db.csv'
    COMMAND = f'srsepc {CONF_CONTAINER_PATH}'
    TUN_CONTROL_PATH = '/dev/net/tun'
    LOG_CONTAINER_PATH = '/tmp/epc.log'
    CAP_CONTAINER_PATH = '/tmp/epc.pcap'
    PING_COMMAND = 'ping {}'

    @staticmethod
    def create(configuration_path: str, hss_db: str, network_id: str, ip: str):
        """
        Create a SrsEPC instance.
        :param configuration_path: SrsEPC configuration path.
        :param hss_db: SrsEPC users DB (HSS configuration) path.
        :param network_id: Docker network to attach to.
        :param ip: Container IP inside the network.
        :return: Epc object.
        :rtype: Epc
        """
        client = docker.from_env()
        volumes = {
            configuration_path: {'bind': Epc.CONF_CONTAINER_PATH, 'mode': 'ro'},
            hss_db: {'bind': Epc.HSS_CONFIGURATION_PATH, 'mode': 'ro'},
            Epc.TUN_CONTROL_PATH: {'bind': Epc.TUN_CONTROL_PATH, 'mode': 'rw'},  # Allow creating TUN devices.
        }
        container = client.containers.create(
            config.epc_docker_image, Epc.COMMAND, volumes=volumes, cap_add=['NET_ADMIN'], auto_remove=True,
            name=Epc.CONTAINER_NAME, network_mode='none'
        )
        epc = Epc(container)
        epc._connect_to_network(network_id, ip)
        container.start()
        epc._wait_for_ip()
        return epc

    def ping(self, ip: str):
        """
        Run ping command inside the container.
        :param ip: IP to ping.
        :return: Socket connected to the ping stdin and stdout.
        :rtype: socket.socket
        """
        _, sock = self._container.exec_run(self.PING_COMMAND.format(ip), stdin=True, socket=True, tty=True)
        return sock._sock
