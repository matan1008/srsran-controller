from srsran_controller.configuration import config
from srsran_controller.mission.epc import Epc
from srsran_controller.srsran_configurations.epc import *


def build_configuration(conf, epc_ip):
    return SrsEpcConfiguration(
        mme=SrsEpcMmeConfiguration(
            mme_code=conf.mme_code, mme_group=conf.mme_group, tac=conf.tac, mcc=conf.mcc, mnc=conf.mnc,
            mme_bind_addr=epc_ip, apn=conf.apn, short_net_name=conf.short_net_name, full_net_name=conf.full_net_name
        ),
        hss=SrsEpcHssConfiguration(db_file=Epc.HSS_CONFIGURATION_PATH),
        spgw=SrsEpcSpgwConfiguration(gtpu_bind_addr=epc_ip, sgi_if_name=Epc.SGI_INTERFACE_NAME),
        pcap=SrsEpcPcapConfiguration(enable=True, filename=Epc.CAP_CONTAINER_PATH),
        log=SrsEpcLogConfiguration(filename=Epc.LOG_CONTAINER_PATH)
    )


def create(conf, lte_network, epc_ip: str, pgw_network=None, pgw_ip: str = '') -> Epc:
    """
    Factory method for Epc objects.
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf: Mission configuration.
    :param lte_network: Network to attach to.
    :param epc_ip: IP inside the lte network.
    :param pgw_network: P-GW network to attach to.
    :param pgw_ip: IP inside the P-GW network.
    :return: Launched Epc object.
    """
    with open(config.current_epc_configuration, 'w') as fd:
        build_configuration(conf, epc_ip).write(fd)
    epc = Epc.create(config.current_epc_configuration, config.users_db)
    epc.connect(lte_network, epc_ip)
    if pgw_network is not None:
        epc.connect(pgw_network, pgw_ip)
    epc.start()
    epc.wait_for_ip()
    return epc
