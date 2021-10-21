from srsran_controller.common.docker.network import Network


class LteNetwork(Network):
    NAME = 'lte_network'
    SUBNET = '192.168.52.0/24'
    GATEWAY = '192.168.52.254'
    INTERFACE_NAME = 'lte-network'

    @classmethod
    def create(cls, name: str = NAME, subnet: str = SUBNET, gateway: str = GATEWAY,
               interface_name: str = INTERFACE_NAME):
        """
        Create a network for LTE entities.
        :param name: Network name.
        :param subnet: Network subnet.
        :param gateway: Network gateway.
        :param interface_name: Interface name on host.
        :return: LteNetwork object.
        :rtype: LteNetwork
        """
        return super().create(name, subnet, gateway, interface_name)
