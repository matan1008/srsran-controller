from srslte_controller.configuration import config
from srslte_controller.mission.epc import Epc
from srslte_controller.mission.lte_network import LteNetwork
from srslte_controller.srslte_configurations.epc import *


def build_configuration(conf, epc_ip):
    return SrsEpcConfiguration(
        mme=SrsEpcMmeConfiguration(
            mme_code=conf.mme_code, mme_group=conf.mme_group, tac=conf.tac, mcc=conf.mcc, mnc=conf.mnc,
            mme_bind_addr=epc_ip, apn=conf.apn
        ),
        hss=SrsEpcHssConfiguration(db_file=Epc.HSS_CONFIGURATION_PATH),
        spgw=SrsEpcSpgwConfiguration(gtpu_bind_addr=epc_ip),
        pcap=SrsEpcPcapConfiguration(enable=True, filename=Epc.CAP_CONTAINER_PATH),
        log=SrsEpcLogConfiguration(filename=Epc.LOG_CONTAINER_PATH, all_level='debug')
    )


def create(conf, epc_ip):
    with open(config.current_epc_configuration, 'w') as fd:
        build_configuration(conf, epc_ip).write(fd)
    return Epc.create(config.current_epc_configuration, config.users_db, LteNetwork.NAME, epc_ip)
