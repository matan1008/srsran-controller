import docker
from docker.types import IPAMPool, IPAMConfig


class Network:
    def __init__(self, network):
        """
        :param docker.models.networks.Network network: Docker network to wrap.
        """
        self._network = network

    @property
    def id(self):
        return self._network.id

    @classmethod
    def create(cls, name: str, subnet: str, gateway: str, interface_name: str):
        """
        Create a network for docker entities.
        :param name: Network name.
        :param subnet: Network subnet.
        :param gateway: Network gateway.
        :param interface_name: Interface name on host.
        :return: Network object.
        :rtype: Network
        """
        client = docker.from_env()
        return cls(client.networks.create(
            name, driver='bridge', options={'com.docker.network.bridge.name': interface_name,
                                            'com.docker.network.container_iface_prefix': interface_name},
            ipam=IPAMConfig(pool_configs=[IPAMPool(subnet=subnet, gateway=gateway)])
        ))

    def shutdown(self):
        self._network.remove()
