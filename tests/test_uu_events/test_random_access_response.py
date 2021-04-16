from pyshark import FileCapture

from srslte_controller.uu_events.random_access_response import create as create_rar

RAR_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff00009300000008497960474e0b001b0000001b000000'
    '01010202000203000004022707010a000f0001530050cc0c004600'
)


def test_parsing_random_access_response(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(RAR_PCAP_DATA))
    pcap = FileCapture(str(p))
    rar = create_rar(list(pcap)[0])
    assert rar == {'event': 'RA Response', 'ta': 5, 'c-rnti': 70}
