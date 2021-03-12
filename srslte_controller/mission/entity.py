import docker
from docker.errors import APIError


class Entity:
    def __init__(self, container):
        """
        Docker container to wrap.
        :param docker.models.containers.Container container:
        """
        self._container = container

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

    def _connect_to_network(self, network_id: str, ip: str):
        """
        Connect the underlying container to a specified docker network, giving it the specified IP address.
        :param network_id: Docker network to attach to.
        :param ip: Container IP inside the network.
        """
        client = docker.from_env()
        client.networks.list(names=['none'])[0].disconnect(self._container)
        client.networks.get(network_id).connect(self._container, ipv4_address=ip)

    def _wait_for_ip(self):
        while not self.ip:
            self._container.reload()
