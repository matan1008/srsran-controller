import docker
from docker.errors import APIError


class Entity:
    def __init__(self, container):
        """
        :param docker.models.containers.Container container: Docker container to wrap.
        """
        self._container = container

    def start(self):
        """
        Start the entity.
        """
        self._container.start()

    @property
    def ip(self) -> str:
        return list(self._container.attrs['NetworkSettings']['Networks'].values())[0]['IPAddress']

    def shutdown(self):
        """
        Kill the underlying docker container and wait for the container to be removed.
        """
        try:
            self._container.kill()
            self._container.wait(condition='removed')
        except APIError:
            # Docker already killed and removed.
            pass

    def connect(self, network, ip: str):
        """
        Connect the underlying container to a specified docker network, giving it the specified IP address.
        :param srsran_controller.mission.network.Network network: Docker network to attach to.
        :param ip: Container IP inside the network.
        """
        client = docker.from_env()
        client.networks.get(network.id).connect(self._container, ipv4_address=ip)

    def wait_for_ip(self):
        """
        Wait for entity to get an IP address.
        """
        while not self.ip:
            self._container.reload()

    def _disconnect(self, network_name):
        client = docker.from_env()
        client.networks.list(names=[network_name])[0].disconnect(self._container)
