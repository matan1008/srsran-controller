import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.nas_emm_attach_request import ATTACH_REQUEST_NAME

ATTACH_REQUEST_IMSI_PCAP_DATA = (
    '0a0d0d0adc0000004d3c2b1a01000000ffffffffffffffff02003b00313174682047656e20496e74656c28522920436f726528544d292069'
    '372d3131373030204020322e353047487a20287769746820535345342e322900030017004c696e757820352e31352e302d35362d67656e65'
    '7269630004005b0044756d70636170202857697265736861726b2920332e362e3720284769742076332e362e37207061636b616765642061'
    '7320332e362e372d317e7562756e747532322e30342e302b77697265736861726b646576737461626c65290000000000dc00000001000000'
    '580000000100000000000400020002006c6f000009000100090000000b000e000075647020706f7274203538343700000c0017004c696e75'
    '7820352e31352e302d35362d67656e6572696300000000005800000006000000a401000000000000226d32178e0ee5798101000081010000'
    '00000000000000000000000008004500017398e440004011a293c0a834027f000001163716d7015fff726d61632d6c746501000302004603'
    '000004026807010a000f00013a3e211f1f35000000a0000020002a0e82e2101220202064a8ed3005e0e000080403a0220000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a4010000'
    '050000006c000000000000003cf00500bff8f8bd01001c00436f756e746572732070726f76696465642062792064756d7063617002000800'
    '3cf00500f71d51b4030008003cf00500a0f8f8bd040008002400000000000000050008000000000000000000000000006c000000'
)

ATTACH_REQUEST_TMSI_PCAP_DATA = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d37373030204350'
    '55204020332e363047487a20287769746820535345342e3229000000030017004c696e757820352e31312e302d33382d67656e6572696300'
    '04003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b6167656420617320332e'
    '322e332d3129000000000000b80000000100000060000000010000000000040002000b006c74652d6e6574776f726b000900010009000000'
    '0b000e000075647020706f7274203538343700000c0017004c696e757820352e31312e302d33382d67656e65726963000000000060000000'
    '06000000a4010000000000003b1bb216f46c2fe281010000810100000242207125110242c0a83402080045000173cef940004011802fc0a8'
    '3402c0a834fe163716d7015febc16d61632d6c746501000302008503000004140807010a000f00013d3a21761f0000a00000203000011a68'
    '17324925b4030741120bf609f10700011a20e839a005f070c0401800290207d0112723808021100100001081060000000083060000000000'
    '0d00000a000005000010000011005209f10700085c0a003103e5e0241309f107000111035758a65d0100e0c1100273c06000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '000000000000000000000000000000000000000000000000a4010000050000006c0000000000000063cf05009384e43501001c00436f756e'
    '746572732070726f76696465642062792064756d706361700200080063cf05005d9bdb190300080063cf05002584e4350400080027060000'
    '00000000050008000000000000000000000000006c000000'
)


def test_parsing_emm_attach_request_imsi(tmp_path):
    p = tmp_path / 'attach_request.pcap'
    p.write_bytes(bytes.fromhex(ATTACH_REQUEST_IMSI_PCAP_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        attach_request = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert attach_request == {
        'imsi': '001010123456789',
        'event': ATTACH_REQUEST_NAME,
        'rnti': 70,
        'time': datetime.datetime(2022, 12, 20, 8, 40, 6, 549246),
        'data': {},
        'enb_ip': '192.168.52.2',
    }


def test_parsing_emm_attach_request_tmsi(tmp_path):
    p = tmp_path / 'attach_request.pcap'
    p.write_bytes(bytes.fromhex(ATTACH_REQUEST_TMSI_PCAP_DATA))
    with FileCapture(str(p), use_json=True) as pcap:
        attach_request = list(EventsFactory().from_packet(list(pcap)[0]))[0]
    assert attach_request == {
        'tmsi': 0x20e839a0,
        'event': ATTACH_REQUEST_NAME,
        'rnti': 133,
        'data': {
            'old_lai': {'mcc': '901', 'mnc': '70', 'lac': 1},
            'old_tai': {'mcc': '901', 'mnc': '70', 'tac': 8},
        },
        'time': datetime.datetime(2021, 10, 28, 8, 39, 18, 700691),
        'enb_ip': '192.168.52.2',
    }
