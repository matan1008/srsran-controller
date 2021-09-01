from ipaddress import IPv4Network

from srsran_controller.common.ip import forward_interfaces
from srsran_controller.common.utils import shutdown_on_error
from srsran_controller.configuration import config
from srsran_controller.mission.lte_network import LteNetwork
from srsran_controller.mission.mission import Mission
from srsran_controller.mission.pgw_network import PgwNetwork
from srsran_controller.mission_factory.enb import create as create_enb
from srsran_controller.mission_factory.epc import create as create_epc


async def create(configuration):
    """
    Create and start a new mission.
    :param srsran_controller.mission.mission_configuration.MissionConfiguration configuration:
    """
    epc_ip, enb_ip = map(str, list(IPv4Network(LteNetwork.SUBNET).hosts())[0:2])

    with shutdown_on_error(LteNetwork.create()) as lte_network:
        external_interface = configuration.external_interface
        if external_interface.lower() == 'none':
            with shutdown_on_error(create_epc(configuration, lte_network, epc_ip)) as epc:
                with shutdown_on_error(create_enb(configuration, lte_network, epc_ip, enb_ip)) as enb:
                    return Mission(epc, enb, lte_network)
        else:
            epc_pgw_ip = str(list(IPv4Network(PgwNetwork.SUBNET).hosts())[0])
            with shutdown_on_error(PgwNetwork.create()) as pgw_network:
                with shutdown_on_error(create_epc(configuration, lte_network, epc_ip, pgw_network, epc_pgw_ip)) as epc:
                    with shutdown_on_error(create_enb(configuration, lte_network, epc_ip, enb_ip)) as enb:
                        epc.ip_forward(pgw_network)
                        forward_interfaces(PgwNetwork.INTERFACE_NAME, external_interface, config.sudo_password)
                        return Mission(epc, enb, lte_network, pgw_network)
