import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.nas_emm_attach_accept import ATTACH_ACCEPT_NAME

ATTACH_ACCEPT_PCAP_DATA_IMSI = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003600496e74656c28522920436f726528544d292069372d363730304b20435'
    '055204020342e303047487a20287769746820535345342e32290000030017004c696e757820352e31312e302d32372d67656e657269630004'
    '003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b6167656420617320332e322'
    'e332d3129000000000000b80000000100000060000000010000000000040002000b006c74652d6e6574776f726b0009000100090000000b00'
    '0e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d32372d67656e6572696300000000006000000006000'
    '000e0000000000000006a099d167e211cf2bd000000bd00000002429a4d39c30242c0a834020800450000af0051400040114f9cc0a83402c0'
    'a834fe163716d7009beafd6d61632d6c746501010302004603000004035407010a000f000121741fa00404201610800000032002801309da4'
    'ae9410041d0804f8180003c440001c007d480704041c2421a5b9d195c9b995d01406b04000089c220000341020202021402fd803c44000046'
    '94f5d92f04c03c44000048c17d14f5d92f189f07d40a63a43c733cb833321834c00026408000f8ab4f613d0000000000e0000000050000006'
    'c00000000000000fec905002fb4318401001c00436f756e746572732070726f76696465642062792064756d7063617002000800fec9050043'
    'e4315003000800fec90500a5b33184040008001800000000000000050008000000000000000000000000006c000000'
)


def test_parsing_emm_attach_accept(tmp_path):
    p = tmp_path / 'attach_accept.pcap'
    p.write_bytes(bytes.fromhex(ATTACH_ACCEPT_PCAP_DATA_IMSI))
    pcap = FileCapture(str(p))
    rar = EventsFactory().from_packet(list(pcap)[0])
    assert rar == {
        'ip': '172.16.0.2',
        'event': ATTACH_ACCEPT_NAME,
        'rnti': 70,
        'time': datetime.datetime(2021, 8, 20, 17, 16, 35, 111101),
    }
