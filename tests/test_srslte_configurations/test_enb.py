from io import StringIO

from srsran_controller.srsran_configurations.enb import *


def test_sanity():
    output = StringIO()
    SrsEnbConfiguration(
        enb=SrsEnbEnbConfiguration(
            enb_id=0x19B, mcc='001', mnc='01', mme_addr='127.0.1.100', gtp_bind_addr='127.0.1.1',
            s1c_bind_addr='127.0.1.1', n_prb=50
        ),
        enb_files=SrsEnbEnbFilesConfiguration(sib_config='sib.conf', rr_config='rr.conf', drb_config='drb.conf'),
        rf=SrsEnbRfConfiguration(),
        pcap=SrsEnbPcapConfiguration(enable=False, filename='/tmp/enb.pcap', s1ap_enable=False,
                                     s1ap_filename='/tmp/enb_s1ap.pcap'),
        log=SrsEnbLogConfiguration(all_hex_limit=32, filename='/tmp/enb.log')
    ).write(output)
    assert output.getvalue() == (
        '[enb]\n'
        'enb_id = 411\n'
        'mcc = 001\n'
        'mnc = 01\n'
        'mme_addr = 127.0.1.100\n'
        'gtp_bind_addr = 127.0.1.1\n'
        's1c_bind_addr = 127.0.1.1\n'
        'n_prb = 50\n'
        '\n'
        '[enb_files]\n'
        'sib_config = sib.conf\n'
        'rr_config = rr.conf\n'
        'drb_config = drb.conf\n'
        '\n'
        '[rf]\n'
        'device_name = auto\n'
        'device_args = auto\n'
        'time_adv_nsamples = auto\n'
        'tx_gain = 80\n'
        'rx_gain = 40\n'
        '\n'
        '[pcap]\n'
        'filename = /tmp/enb.pcap\n'
        's1ap_filename = /tmp/enb_s1ap.pcap\n'
        'enable = False\n'
        's1ap_enable = False\n'
        '\n'
        '[log]\n'
        'rf_level = info\n'
        'phy_level = info\n'
        'phy_lib_level = info\n'
        'mac_level = info\n'
        'rlc_level = info\n'
        'pdcp_level = info\n'
        'rrc_level = info\n'
        'gtpu_level = info\n'
        's1ap_level = info\n'
        'stack_level = info\n'
        'filename = /tmp/enb.log\n'
        'all_hex_limit = 32\n'
        'file_max_size = -1\n'
        '\n'
    )


def test_log_all():
    output = StringIO()
    SrsEnbConfiguration(
        enb=SrsEnbEnbConfiguration(
            enb_id=0x19B, mcc='001', mnc='01', mme_addr='127.0.1.100', gtp_bind_addr='127.0.1.1',
            s1c_bind_addr='127.0.1.1', n_prb=50
        ),
        enb_files=SrsEnbEnbFilesConfiguration(sib_config='sib.conf', rr_config='rr.conf', drb_config='drb.conf'),
        rf=SrsEnbRfConfiguration(),
        pcap=SrsEnbPcapConfiguration(enable=False, filename='/tmp/enb.pcap', s1ap_enable=False,
                                     s1ap_filename='/tmp/enb_s1ap.pcap'),
        log=SrsEnbLogConfiguration(all_hex_limit=32, filename='/tmp/enb.log', all_level='debug')
    ).write(output)
    assert output.getvalue() == (
        '[enb]\n'
        'enb_id = 411\n'
        'mcc = 001\n'
        'mnc = 01\n'
        'mme_addr = 127.0.1.100\n'
        'gtp_bind_addr = 127.0.1.1\n'
        's1c_bind_addr = 127.0.1.1\n'
        'n_prb = 50\n'
        '\n'
        '[enb_files]\n'
        'sib_config = sib.conf\n'
        'rr_config = rr.conf\n'
        'drb_config = drb.conf\n'
        '\n'
        '[rf]\n'
        'device_name = auto\n'
        'device_args = auto\n'
        'time_adv_nsamples = auto\n'
        'tx_gain = 80\n'
        'rx_gain = 40\n'
        '\n'
        '[pcap]\n'
        'filename = /tmp/enb.pcap\n'
        's1ap_filename = /tmp/enb_s1ap.pcap\n'
        'enable = False\n'
        's1ap_enable = False\n'
        '\n'
        '[log]\n'
        'filename = /tmp/enb.log\n'
        'all_hex_limit = 32\n'
        'all_level = debug\n'
        'file_max_size = -1\n'
        '\n'
    )
