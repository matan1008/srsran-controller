import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.random_access_response import RA_RESPONSE_NAME

RAR_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff0000950000000ac78b60dfd602002a0000002a000000beefdead002a00006d61632d6c746501'
    '010202000203000004024707010a000f0001740050ce0c004600'
)


def test_parsing_random_access_response(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(RAR_PCAP_DATA))
    with FileCapture(str(p)) as pcap:
        rar = EventsFactory().from_packet(list(pcap)[0])
    assert rar == {
        'event': RA_RESPONSE_NAME,
        'ta': 5,
        'c-rnti': 70,
        'time': datetime.datetime(2021, 4, 30, 11, 59, 54, 186079),
    }
