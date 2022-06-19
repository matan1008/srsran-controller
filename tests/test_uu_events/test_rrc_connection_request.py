import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.rrc_connection_request import CONNECTION_REQUEST_NAME

RRC_CONNECTION_REQUEST_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff00009500000013cb8b6047e908002900000029000000beefdead002900006d61632d6c746501'
    '0003020047030000041a0207010a000f00010041a1c1192e76'
)


def test_parsing_connection_request_with_tmsi(tmp_path):
    p = tmp_path / 'rrc_connection_request.pcap'
    p.write_bytes(bytes.fromhex(RRC_CONNECTION_REQUEST_PCAP_DATA))
    with FileCapture(str(p)) as pcap:
        connection_request = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert connection_request == {
        'event': CONNECTION_REQUEST_NAME,
        'tmsi': 0x1c1192e7,
        'rnti': 71,
        'time': datetime.datetime(2021, 4, 30, 12, 17, 7, 584007),
    }
