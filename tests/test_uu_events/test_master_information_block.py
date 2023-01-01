import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.master_information_block import MIB_NAME

GSM_MIB_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d373730302043'
    '5055204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33372d67656e657269'
    '630004003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b61676564206173'
    '20332e322e332d3129000000000000b800000001000000580000000100000000000400020002006c6f000009000100090000000b000e00'
    '0075647020706f7274203538343700000c0017004c696e757820352e31312e302d33372d67656e65726963000000000058000000060000'
    '0068000000000000008f44ad160feca4e9470000004700000000000000000000000000000008004500003932c24000401109f07f000001'
    '7f000001163716d70025fe386d61632d6c746501010002000003000004040807010a000f00018599510068000000050000006c00000000'
    '00000026ce05008d696c1601001c00436f756e746572732070726f76696465642062792064756d706361700200080026ce0500f08b1006'
    '0300080026ce0500b5686c16040008000600000000000000050008000000000000000000000000006c000000'
)


def test_parsing_mib(tmp_path):
    p = tmp_path / 'mib.pcap'
    p.write_bytes(bytes.fromhex(GSM_MIB_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        mib = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert mib == {
        'event': MIB_NAME,
        'data': {
            'phich_duration': 'normal',
            'phich_resource': '1/2',
            'downlink_bandwidth': 75,
        },
        'time': datetime.datetime(2021, 10, 12, 14, 20, 24, 696270),
        'enb_ip': '127.0.0.1',
    }
