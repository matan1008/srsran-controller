from io import StringIO

from srsran_controller.srsran_configurations.epc import *


def test_sanity():
    output = StringIO()
    SrsEpcConfiguration(
        mme=SrsEpcMmeConfiguration(
            mme_code='0x1a', mme_group='0x0001', tac=0x0007, mcc='001', mnc='01', mme_bind_addr='127.0.1.100',
            apn='srsapn', dns_addr='8.8.8.8', encryption_algo='EEA0', integrity_algo='EIA1', paging_timer=2
        ),
        hss=SrsEpcHssConfiguration(db_file='user_db.csv'),
        spgw=SrsEpcSpgwConfiguration(
            gtpu_bind_addr='127.0.1.100', sgi_if_addr='172.16.0.1', sgi_if_name='srs_spgw_sgi', max_paging_queue=100
        ),
        pcap=SrsEpcPcapConfiguration(enable=False, filename='/tmp/epc.pcap'),
        log=SrsEpcLogConfiguration(
            all_hex_limit=32, filename='/tmp/epc.log', nas_level='debug', s1ap_level='debug', mme_gtpc_level='debug',
            spgw_gtpc_level='debug', gtpu_level='debug', spgw_level='debug', hss_level='debug'
        )
    ).write(output)
    assert output.getvalue() == (
        '[mme]\n'
        'mme_code = 0x1a\n'
        'mme_group = 0x0001\n'
        'tac = 7\n'
        'mcc = 001\n'
        'mnc = 01\n'
        'mme_bind_addr = 127.0.1.100\n'
        'apn = srsapn\n'
        'dns_addr = 8.8.8.8\n'
        'encryption_algo = EEA0\n'
        'integrity_algo = EIA1\n'
        'paging_timer = 2\n'
        '\n'
        '[hss]\n'
        'db_file = user_db.csv\n'
        '\n'
        '[spgw]\n'
        'gtpu_bind_addr = 127.0.1.100\n'
        'sgi_if_addr = 172.16.0.1\n'
        'sgi_if_name = srs_spgw_sgi\n'
        'max_paging_queue = 100\n'
        '\n'
        '[pcap]\n'
        'filename = /tmp/epc.pcap\n'
        'enable = False\n'
        '\n'
        '[log]\n'
        'nas_level = debug\n'
        's1ap_level = debug\n'
        'mme_gtpc_level = debug\n'
        'spgw_gtpc_level = debug\n'
        'gtpu_level = debug\n'
        'spgw_level = debug\n'
        'hss_level = debug\n'
        'filename = /tmp/epc.log\n'
        'all_hex_limit = 32\n'
        '\n'
    )


def test_log_all():
    output = StringIO()
    SrsEpcConfiguration(
        mme=SrsEpcMmeConfiguration(
            mme_code='0x1a', mme_group='0x0001', tac=0x0007, mcc='001', mnc='01', mme_bind_addr='127.0.1.100',
            apn='srsapn', dns_addr='8.8.8.8', encryption_algo='EEA0', integrity_algo='EIA1', paging_timer=2
        ),
        hss=SrsEpcHssConfiguration(db_file='user_db.csv'),
        spgw=SrsEpcSpgwConfiguration(
            gtpu_bind_addr='127.0.1.100', sgi_if_addr='172.16.0.1', sgi_if_name='srs_spgw_sgi', max_paging_queue=100
        ),
        pcap=SrsEpcPcapConfiguration(enable=False, filename='/tmp/epc.pcap'),
        log=SrsEpcLogConfiguration(all_hex_limit=32, filename='/tmp/epc.log', all_level='info')
    ).write(output)
    assert output.getvalue() == (
        '[mme]\n'
        'mme_code = 0x1a\n'
        'mme_group = 0x0001\n'
        'tac = 7\n'
        'mcc = 001\n'
        'mnc = 01\n'
        'mme_bind_addr = 127.0.1.100\n'
        'apn = srsapn\n'
        'dns_addr = 8.8.8.8\n'
        'encryption_algo = EEA0\n'
        'integrity_algo = EIA1\n'
        'paging_timer = 2\n'
        '\n'
        '[hss]\n'
        'db_file = user_db.csv\n'
        '\n'
        '[spgw]\n'
        'gtpu_bind_addr = 127.0.1.100\n'
        'sgi_if_addr = 172.16.0.1\n'
        'sgi_if_name = srs_spgw_sgi\n'
        'max_paging_queue = 100\n'
        '\n'
        '[pcap]\n'
        'filename = /tmp/epc.pcap\n'
        'enable = False\n'
        '\n'
        '[log]\n'
        'filename = /tmp/epc.log\n'
        'all_hex_limit = 32\n'
        'all_level = info\n'
        '\n'
    )
