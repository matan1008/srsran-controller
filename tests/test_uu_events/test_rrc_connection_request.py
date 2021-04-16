from pyshark import FileCapture

from srslte_controller.uu_events.rrc_connection_request import create as create_rrc_conn_request

RRC_CONNECTION_REQUEST_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff00009300000094867960312c09001a0000001a00000001000302004703000004'
    '238207010a000f00010041a7ec0c4664'
)


def test_parsing_connection_request_with_tmsi(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(RRC_CONNECTION_REQUEST_PCAP_DATA))
    pcap = FileCapture(str(p))
    rar = create_rrc_conn_request(list(pcap)[0])
    assert rar == {'event': 'RRC connection request', 'tmsi': '7ec0c466', 'rnti': 71}
