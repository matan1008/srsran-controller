from srsran_controller.common.docker.network import Network


class PgwNetwork(Network):
    NAME = 'pgw_network'
    SUBNET = '192.169.52.0/24'
    GATEWAY = '192.169.52.254'
    INTERFACE_NAME = 'pgw-network'

    @classmethod
    def create(cls, name: str = NAME, subnet: str = SUBNET, gateway: str = GATEWAY,
               interface_name: str = INTERFACE_NAME):
        """
        Create a network for connecting the EPC to the internet.
        :param name: Network name.
        :param subnet: Network subnet.
        :param gateway: Network gateway.
        :param interface_name: Interface name on host.
        :return: PgwNetwork object.
        :rtype: PgwNetwork
        """
        return super().create(name, subnet, gateway, interface_name)
