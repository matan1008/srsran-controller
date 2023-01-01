from contextlib import ExitStack
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
    epc_ip = str(list(IPv4Network(LteNetwork.SUBNET).hosts())[0])
    enb_ips = [str(ip) for ip in list(IPv4Network(LteNetwork.SUBNET).hosts())[1:len(configuration.cells) + 1]]
    epc_pgw_ip = str(list(IPv4Network(PgwNetwork.SUBNET).hosts())[0])
    pgw_interface = configuration.external_interface

    with ExitStack() as stack:
        lte_network = stack.enter_context(shutdown_on_error(LteNetwork.create()))
        pgw_network = (
            stack.enter_context(shutdown_on_error(PgwNetwork.create())) if pgw_interface.lower() != 'none' else None
        )
        epc = stack.enter_context(
            shutdown_on_error(create_epc(configuration, lte_network, epc_ip, pgw_network, epc_pgw_ip))
        )
        enbs = []
        for i in range(len(configuration.cells)):
            enbs.append(stack.enter_context(
                shutdown_on_error(create_enb(configuration, i, lte_network, epc_ip, enb_ips[i]))
            ))
        if pgw_interface.lower() != 'none':
            epc.ip_forward(pgw_network)
            forward_interfaces(PgwNetwork.INTERFACE_NAME, pgw_interface, config.sudo_password)
        return Mission(configuration, epc, enbs, lte_network, pgw_network)
