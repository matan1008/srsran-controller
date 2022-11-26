import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.random_access_response import RA_RESPONSE_NAME

RAR_PCAP_DATA = (
    'd4c3b2a1020004000000000000000000ffff0000950000000ac78b60dfd602002a0000002a000000beefdead002a00006d61632d6c746501'
    '010202000203000004024707010a000f0001740050ce0c004600'
)

MULTIPLE_RAR_PCAP_DATA = (
    '0a0d0d0adc0000004d3c2b1a01000000ffffffffffffffff02003b00313174682047656e20496e74656c28522920436f726528544d292069'
    '372d3131373030204020322e353047487a20287769746820535345342e322900030017004c696e757820352e31352e302d35322d67656e65'
    '7269630004005b0044756d70636170202857697265736861726b2920332e362e3720284769742076332e362e37207061636b616765642061'
    '7320332e362e372d317e7562756e747532322e30342e302b77697265736861726b646576737461626c65290000000000dc00000001000000'
    '58000000710000000000040002000300616e790009000100090000000b000e000075647020706f7274203538343700000c0017004c696e75'
    '7820352e31352e302d35322d67656e65726963000000000058000000060000007800000000000000b98d2a17bd9b4f7c5500000055000000'
    '0003000100060242c0a834020000080045000045a2e440004011ad72c0a83402c0a834fe163716d70031ea936d61632d6c74650101020200'
    '0203000004155607010a000f0001de690051980c006b00119e0c006c0000000078000000050000006c0000000000000038ee05005775f2d0'
    '01001c00436f756e746572732070726f76696465642062792064756d706361700200080035ee0500d13bf8cb0300080038ee05005675f2d0'
    '040008008a10000000000000050008000000000000000000000000006c000000'
)


def test_parsing_random_access_response(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(RAR_PCAP_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        rar = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert rar == {
        'event': RA_RESPONSE_NAME,
        'ta': 5,
        'c-rnti': 70,
        'time': datetime.datetime(2021, 4, 30, 11, 59, 54, 186079),
    }


def test_parsing_multiple_random_access_response(tmp_path):
    p = tmp_path / 'random_access_response.pcap'
    p.write_bytes(bytes.fromhex(MULTIPLE_RAR_PCAP_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        rar = list(EventsFactory().from_packet(list(pcap)[0]))
    assert rar == [
        {
            'event': RA_RESPONSE_NAME,
            'ta': 5,
            'c-rnti': 107,
            'time': datetime.datetime(2022, 11, 24, 17, 7, 19, 688248),
        }, {
            'event': RA_RESPONSE_NAME,
            'ta': 1,
            'c-rnti': 108,
            'time': datetime.datetime(2022, 11, 24, 17, 7, 19, 688248),
        }
    ]
