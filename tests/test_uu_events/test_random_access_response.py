from pyshark import FileCapture

from srsran_controller.uu_events.random_access_response import create as create_rar

RAR_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff0000950000000ac78b60dfd602002a0000002a000000beefdead002a00006d61632d6c746501'
    '010202000203000004024707010a000f0001740050ce0c004600'
)


def test_parsing_random_access_response(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(RAR_PCAP_DATA))
    pcap = FileCapture(str(p))
    rar = create_rar(list(pcap)[0])
    assert rar == {'event': 'RA Response', 'ta': 5, 'c-rnti': 70}
