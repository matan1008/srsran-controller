from ipaddress import IPv4Network

from srslte_controller.configuration import config
from srslte_controller.mission.enb import Enb
from srslte_controller.mission.epc import Epc
from srslte_controller.mission.lte_network import LteNetwork
from srslte_controller.mission.mission import Mission
from srslte_controller.srslte_configurations.enb import *
from srslte_controller.srslte_configurations.enb_drbs import *
from srslte_controller.srslte_configurations.enb_rr import *
from srslte_controller.srslte_configurations.enb_sibs import *
from srslte_controller.srslte_configurations.epc import *


class MissionFactory:
    @staticmethod
    def create(configuration):
        """
        Create and start a new mission.
        :param srslte_controller.mission.mission_configuration.MissionConfiguration configuration:
        """
        network = LteNetwork.create()
        epc_ip, enb_ip = map(str, list(IPv4Network(LteNetwork.SUBNET).hosts())[0:2])

        try:
            epc = MissionFactory._create_epc(configuration, epc_ip)
        except Exception:
            network.shutdown()
            raise

        try:
            enb = MissionFactory._create_enb(configuration, epc_ip, enb_ip)
        except Exception:
            epc.shutdown()
            network.shutdown()
            raise

        return Mission(epc, enb, network)

    @staticmethod
    def _create_epc(conf, epc_ip):
        configuration = SrsEpcConfiguration(
            mme=SrsEpcMmeConfiguration(
                mme_code=conf.mme_code, mme_group=conf.mme_group, tac=conf.tac, mcc=conf.mcc, mnc=conf.mnc,
                mme_bind_addr=epc_ip, apn=conf.apn
            ),
            hss=SrsEpcHssConfiguration(db_file=Epc.HSS_CONFIGURATION_PATH),
            spgw=SrsEpcSpgwConfiguration(gtpu_bind_addr=epc_ip),
            pcap=SrsEpcPcapConfiguration(enable=True, filename=Epc.CAP_CONTAINER_PATH),
            log=SrsEpcLogConfiguration(filename=Epc.LOG_CONTAINER_PATH, all_level='debug')
        )
        with open(config.current_epc_configuration, 'w') as fd:
            configuration.write(fd)
        return Epc.create(config.current_epc_configuration, config.users_db, LteNetwork.NAME, epc_ip)

    @staticmethod
    def _create_enb_sibs(conf):
        gsm_neighbors = tuple(
            SrsEnbSib7CarrierFreqsInfo(
                start_arfcn=neighbor.arfcn, band_ind=neighbor.band, explicit_list_of_arfcns=(neighbor.arfcn,)
            )
            for neighbor in conf.gsm_neighbors
        )
        configuration = SrsEnbSibs(sib7=SrsEnbSib7(carrier_freqs_info_list=gsm_neighbors))
        with open(config.current_enb_sibs_configuration, 'w') as fd:
            configuration.write(fd)

    @staticmethod
    def _create_enb_drbs():
        configuration = SrsEnbDrbs(qci_config=(
            SrsEnbDrbQciConfig(
                qci=7,
                pdcp_config=SrsEnbDrbQciConfigPdcpConfig(discard_timer=100, pdcp_sn_size=12),
                rlc_config=SrsEnbDrbQciConfigRlcConfig(
                    ul_um=SrsEnbDrbQciConfigRlcConfigUlUm(sn_field_length=10),
                    dl_um=SrsEnbDrbQciConfigRlcConfigDlUm(sn_field_length=10, t_reordering=45)
                ),
                logical_channel_config=SrsEnbDrbQciConfigLogicalChannelConfig(
                    priority=13, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=2
                )
            ),
            SrsEnbDrbQciConfig(
                qci=9,
                pdcp_config=SrsEnbDrbQciConfigPdcpConfig(discard_timer=-1, status_report_required=True),
                rlc_config=SrsEnbDrbQciConfigRlcConfig(
                    ul_am=SrsEnbDrbQciConfigRlcConfigUlAm(t_poll_retx=120, poll_pdu=64, poll_byte=750,
                                                          max_retx_thresh=16),
                    dl_am=SrsEnbDrbQciConfigRlcConfigDlAm(t_reordering=50, t_status_prohibit=50)
                ),
                logical_channel_config=SrsEnbDrbQciConfigLogicalChannelConfig(
                    priority=11, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=3
                )
            ),
        ))
        with open(config.current_enb_drbs_configuration, 'w') as fd:
            configuration.write(fd)

    @staticmethod
    def _create_enb_rr(conf):
        configuration = SrsEnbRR(
            cell_list=(SrsEnbRRCell(
                cell_id=conf.cell_id, tac=conf.tac, pci=conf.pci, dl_earfcn=conf.earfcn,
                meas_cell_list=(SrsEnbRRCellListMeasCell(eci=(256 * conf.enb_id) + 0x01, dl_earfcn=3350, pci=1),),
                meas_report_desc=SrsEnbRRCellListMeasReportDesc()
            ),)
        )
        with open(config.current_enb_rr_configuration, 'w') as fd:
            configuration.write(fd)

    @staticmethod
    def _create_enb_rf_configuration(conf):
        """
        :param srslte_controller.mission.mission_configuration.MissionConfiguration conf:
        """
        args = conf.device_args
        if conf.device_name == 'zmq':
            args = (
                'fail_on_disconnect=true,'
                f'tx_port=tcp://*:2000,rx_port=tcp://{LteNetwork.GATEWAY}:2001,id=enb,base_srate=23.04e6'
            )
        return SrsEnbRfConfiguration(device_name=conf.device_name, device_args=args)

    @staticmethod
    def _create_enb(conf, epc_ip, enb_ip):
        MissionFactory._create_enb_sibs(conf)
        MissionFactory._create_enb_drbs()
        MissionFactory._create_enb_rr(conf)
        configuration = SrsEnbConfiguration(
            enb=SrsEnbEnbConfiguration(
                enb_id=conf.enb_id, mcc=conf.mcc, mnc=conf.mnc, mme_addr=epc_ip, gtp_bind_addr=enb_ip,
                s1c_bind_addr=enb_ip
            ),
            enb_files=SrsEnbEnbFilesConfiguration(sib_config=Enb.SIBS_CONF_CONTAINER_PATH,
                                                  rr_config=Enb.RR_CONF_CONTAINER_PATH,
                                                  drb_config=Enb.DRBS_CONF_CONTAINER_PATH),
            rf=MissionFactory._create_enb_rf_configuration(conf),
            pcap=SrsEnbPcapConfiguration(filename=Enb.CAP_CONTAINER_PATH, s1ap_enable=False, s1ap_filename=''),
            log=SrsEnbLogConfiguration(filename=Enb.LOG_CONTAINER_PATH, all_level='info')
        )
        with open(config.current_enb_configuration, 'w') as fd:
            configuration.write(fd)
        return Enb.create(
            config.current_enb_configuration, config.current_enb_sibs_configuration,
            config.current_enb_drbs_configuration, config.current_enb_rr_configuration, LteNetwork.NAME, enb_ip
        )
