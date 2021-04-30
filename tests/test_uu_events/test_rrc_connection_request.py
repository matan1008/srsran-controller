from pyshark import FileCapture

from srsran_controller.uu_events.rrc_connection_request import create as create_rrc_conn_request

RRC_CONNECTION_REQUEST_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff00009500000013cb8b6047e908002900000029000000beefdead002900006d61632d6c746501'
    '0003020047030000041a0207010a000f00010041a1c1192e76'
)


def test_parsing_connection_request_with_tmsi(tmp_path):
    p = tmp_path / 'rrc_connection_request.pcap'
    p.write_bytes(bytes.fromhex(RRC_CONNECTION_REQUEST_PCAP_DATA))
    pcap = FileCapture(str(p))
    rar = create_rrc_conn_request(list(pcap)[0])
    assert rar == {'event': 'RRC connection request', 'tmsi': '1c1192e7', 'rnti': 71}
