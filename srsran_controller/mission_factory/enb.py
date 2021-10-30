from srsran_controller.configuration import config
from srsran_controller.mission.enb import Enb
from srsran_controller.mission.lte_network import LteNetwork
from srsran_controller.srsran_configurations.enb import *
from srsran_controller.srsran_configurations.enb_rbs import *
from srsran_controller.srsran_configurations.enb_rr import *
from srsran_controller.srsran_configurations.enb_sibs import *


def build_sibs(conf):
    gsm_neighbors = tuple(
        SrsEnbSib7CarrierFreqsInfo(
            start_arfcn=neighbor.arfcn, band_ind=neighbor.band, explicit_list_of_arfcns=(neighbor.arfcn,)
        )
        for neighbor in conf.gsm_neighbors
    )
    return SrsEnbSibs(sib7=SrsEnbSib7(carrier_freqs_info_list=gsm_neighbors))


def build_rbs():
    return SrsEnbRbs(qci_config=(
        SrsEnbRbQciConfig(
            qci=7,
            pdcp_config=SrsEnbRbQciConfigPdcpConfig(discard_timer=100, pdcp_sn_size=12),
            rlc_config=SrsEnbRbQciConfigRlcConfig(
                ul_um=SrsEnbRbQciConfigRlcConfigUlUm(sn_field_length=10),
                dl_um=SrsEnbRbQciConfigRlcConfigDlUm(sn_field_length=10, t_reordering=45)
            ),
            logical_channel_config=SrsEnbRbQciConfigLogicalChannelConfig(
                priority=13, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=2
            )
        ),
        SrsEnbRbQciConfig(
            qci=9,
            pdcp_config=SrsEnbRbQciConfigPdcpConfig(discard_timer=-1, status_report_required=True),
            rlc_config=SrsEnbRbQciConfigRlcConfig(
                ul_am=SrsEnbRbQciConfigRlcConfigUlAm(t_poll_retx=120, poll_pdu=64, poll_byte=750,
                                                      max_retx_thresh=16),
                dl_am=SrsEnbRbQciConfigRlcConfigDlAm(t_reordering=50, t_status_prohibit=50)
            ),
            logical_channel_config=SrsEnbRbQciConfigLogicalChannelConfig(
                priority=11, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=3
            )
        ),
    ))


def build_rr(conf):
    """
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf:
    """
    return SrsEnbRR(
        cell_list=tuple(SrsEnbRRCell(
            cell_id=cell.cell_id, tac=conf.tac, pci=cell.pci, dl_earfcn=cell.earfcn, rf_port=i,
            meas_cell_list=(
                SrsEnbRRCellListMeasCell(eci=(256 * conf.enb_id) + cell.cell_id, dl_earfcn=cell.earfcn, pci=cell.pci, ),
            ),
            meas_report_desc=SrsEnbRRCellListMeasReportDesc()
        ) for i, cell in enumerate(conf.cells))
    )


def build_rf_configuration(conf):
    """
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf:
    """
    args = conf.device_args
    if conf.device_name == 'zmq':
        args = (
            'fail_on_disconnect=true,'
            f'tx_port=tcp://*:2000,rx_port=tcp://{LteNetwork.GATEWAY}:2001,id=enb,base_srate=23.04e6'
        )
    return SrsEnbRfConfiguration(device_name=conf.device_name, device_args=args)


def build_configuration(conf, epc_ip, enb_ip):
    return SrsEnbConfiguration(
        enb=SrsEnbEnbConfiguration(
            enb_id=conf.enb_id, mcc=conf.mcc, mnc=conf.mnc, mme_addr=epc_ip, gtp_bind_addr=enb_ip,
            s1c_bind_addr=enb_ip
        ),
        enb_files=SrsEnbEnbFilesConfiguration(sib_config=Enb.SIBS_CONF_CONTAINER_PATH,
                                              rr_config=Enb.RR_CONF_CONTAINER_PATH,
                                              rb_config=Enb.RBS_CONF_CONTAINER_PATH),
        rf=build_rf_configuration(conf),
        pcap=SrsEnbPcapConfiguration(mac_net_enable=True, client_ip=LteNetwork.GATEWAY),
        log=SrsEnbLogConfiguration(filename=Enb.LOG_CONTAINER_PATH, all_level='debug')
    )


def create(conf, lte_network, epc_ip, enb_ip):
    """
    Factory method for Enb objects.
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf: Mission configuration.
    :param lte_network: Network to attach to.
    :param epc_ip: EPC IP inside the lte network.
    :param enb_ip: IP inside the lte network.
    :return: Launched Epc object.
    """
    with open(config.current_enb_sibs_configuration, 'w') as fd:
        build_sibs(conf).write(fd)
    with open(config.current_enb_rbs_configuration, 'w') as fd:
        build_rbs().write(fd)
    with open(config.current_enb_rr_configuration, 'w') as fd:
        build_rr(conf).write(fd)
    with open(config.current_enb_configuration, 'w') as fd:
        build_configuration(conf, epc_ip, enb_ip).write(fd)
    enb = Enb.create(
        config.current_enb_configuration, config.current_enb_sibs_configuration,
        config.current_enb_rbs_configuration, config.current_enb_rr_configuration
    )
    enb.connect(lte_network, enb_ip)
    enb.start()
    enb.wait_for_ip()
    return enb
