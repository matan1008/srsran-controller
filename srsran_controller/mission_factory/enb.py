from srsran_controller.configuration import config
from srsran_controller.mission.enb import Enb
from srsran_controller.mission.lte_network import LteNetwork
from srsran_controller.srsran_configurations.enb import *
from srsran_controller.srsran_configurations.enb_rbs import *
from srsran_controller.srsran_configurations.enb_rr import *
from srsran_controller.srsran_configurations.enb_sibs import *


def build_sibs(conf):
    scheduled_sibs = [3]
    sib4 = None
    sib7 = None
    if conf.intra_freq_neighbours:
        intra_freq_neighs = tuple(
            SrsEnbSib4IntraFreqNeighCellInfo(n.phys_cell_id, n.q_offset_cell) for n in conf.intra_freq_neighbours
        )
        sib4 = SrsEnbSib4(intra_freq_neigh_cell_list=intra_freq_neighs)
        scheduled_sibs.append(4)
    if conf.gsm_neighbours:
        gsm_neighbours = tuple(
            SrsEnbSib7CarrierFreqsInfo(start_arfcn=n.arfcn, band_ind=n.band, explicit_list_of_arfcns=(n.arfcn,))
            for n in conf.gsm_neighbours
        )
        sib7 = SrsEnbSib7(carrier_freqs_info_list=gsm_neighbours)
        scheduled_sibs.append(7)
    sib1 = SrsEnbSib1(sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=scheduled_sibs),))
    return SrsEnbSibs(sib1=sib1, sib4=sib4, sib7=sib7)


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


def build_rr(conf, enb_index):
    """
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf:
    :param enb_index: Index of current enb.
    """
    cell = conf.cells[enb_index]
    conf_cell = SrsEnbRRCell(cell_id=cell.cell_id, tac=conf.tac, pci=cell.pci, dl_earfcn=cell.earfcn)
    if enb_index == 0 and len(conf.cells) > 1:
        ho_cell = conf.cells[1]
        conf_cell.ho_active = True
        conf_cell.meas_cell_list = (
            SrsEnbRRCellListMeasCell(eci=(256 * conf.enb_id) + ho_cell.cell_id, dl_earfcn=ho_cell.earfcn,
                                     pci=ho_cell.pci),)
        conf_cell.meas_report_desc = (SrsEnbRRCellListMeasReportDesc(),)
        conf_cell.meas_quant_desc = SrsEnbRRCellListMeasQuantDesc()
    return SrsEnbRR(cell_list=(conf_cell,))


def build_rf_configuration(conf):
    """
    :param srsran_controller.mission.mission_configuration.EnbCell conf:
    """
    args = conf.device_args + ', ' + conf.device_serial
    if conf.device_name == 'zmq':
        args = (
            'fail_on_disconnect=true,'
            f'tx_port=tcp://*:2000,rx_port=tcp://{LteNetwork.GATEWAY}:2001,id=enb,base_srate=23.04e6'
        )
    return SrsEnbRfConfiguration(device_name=conf.device_name, device_args=args)


def build_configuration(conf, epc_ip, enb_ip, index_):
    return SrsEnbConfiguration(
        enb=SrsEnbEnbConfiguration(
            enb_id=conf.enb_id + index_, mcc=conf.mcc, mnc=conf.mnc, mme_addr=epc_ip, gtp_bind_addr=enb_ip,
            s1c_bind_addr=enb_ip
        ),
        enb_files=SrsEnbEnbFilesConfiguration(sib_config=Enb.SIBS_CONF_CONTAINER_PATH,
                                              rr_config=Enb.RR_CONF_CONTAINER_PATH,
                                              rb_config=Enb.RBS_CONF_CONTAINER_PATH),
        rf=build_rf_configuration(conf.cells[index_]),
        pcap=SrsEnbPcapConfiguration(mac_net_enable=True, client_ip=LteNetwork.GATEWAY),
        log=SrsEnbLogConfiguration(filename=Enb.LOG_CONTAINER_PATH)
    )


def create(conf, enb_index: int, lte_network, epc_ip, enb_ip):
    """
    Factory method for Enb objects.
    :param srsran_controller.mission.mission_configuration.MissionConfiguration conf: Mission configuration.
    :param enb_index: Index of current enb.
    :param lte_network: Network to attach to.
    :param epc_ip: EPC IP inside the lte network.
    :param enb_ip: IP inside the lte network.
    :return: Launched Epc object.
    """
    config.current_enb_sibs_configuration[enb_index].write_text(str(build_sibs(conf)))
    config.current_enb_rbs_configuration[enb_index].write_text(str(build_rbs()))
    config.current_enb_rr_configuration[enb_index].write_text(str(build_rr(conf, enb_index)))
    config.current_enb_configuration[enb_index].write_text(str(build_configuration(conf, epc_ip, enb_ip, enb_index)))
    enb = Enb.create(
        config.current_enb_configuration[enb_index], config.current_enb_sibs_configuration[enb_index],
        config.current_enb_rbs_configuration[enb_index], config.current_enb_rr_configuration[enb_index], enb_index
    )
    enb.connect(lte_network, enb_ip)
    enb.start()
    enb.wait_for_ip()
    return enb
