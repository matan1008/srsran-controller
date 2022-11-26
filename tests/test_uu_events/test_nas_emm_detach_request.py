import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory

DETACH_REQUEST_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff0000950000001dcb8b604daf03003702000037020000beefdead023700006d61632d6c746501'
    '0003020047030000042be807010a000f00013d3a221f1f0935a000004802a2eb378a386060e8a1217ec01e220000234382325ce091cc210a'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
)


def test_parsing_emm_detach_request(tmp_path):
    p = tmp_path / 'detach_request.pcap'
    p.write_bytes(bytes.fromhex(DETACH_REQUEST_PCAP_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        detach = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert detach == {
        'tmsi': 0x1c1192e7,
        'event': 'Detach request',
        'rnti': 71,
        'time': datetime.datetime(2021, 4, 30, 12, 17, 17, 241485),
    }
