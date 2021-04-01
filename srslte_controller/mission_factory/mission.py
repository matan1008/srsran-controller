from ipaddress import IPv4Network

from srslte_controller.common.utils import shutdown_on_error
from srslte_controller.mission.lte_network import LteNetwork
from srslte_controller.mission.mission import Mission
from srslte_controller.mission_factory.enb import create as create_enb
from srslte_controller.mission_factory.epc import create as create_epc


async def create(configuration):
    """
    Create and start a new mission.
    :param srslte_controller.mission.mission_configuration.MissionConfiguration configuration:
    """
    epc_ip, enb_ip = map(str, list(IPv4Network(LteNetwork.SUBNET).hosts())[0:2])

    with shutdown_on_error(LteNetwork.create()) as network:
        with shutdown_on_error(create_epc(configuration, epc_ip)) as epc:
            with shutdown_on_error(create_enb(configuration, epc_ip, enb_ip)) as enb:
                return Mission(epc, enb, network)
