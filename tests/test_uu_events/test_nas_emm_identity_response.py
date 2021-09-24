import datetime

from pyshark import FileCapture

from srsran_controller.uu_events.factory import EventsFactory
from srsran_controller.uu_events.nas_emm_identity_response import IDENTITY_RESPONSE_NAME

IDENTITY_RESPONSE_PCAP_DATA_IMSI = (
    '0a0d0d0ab80000004d3c2b1a01000000ffffffffffffffff02003500496e74656c28522920436f726528544d292069372d343737302043505'
    '5204020332e343047487a20287769746820535345342e3229000000030016004c696e757820352e382e302d35392d67656e65726963000004'
    '003a0044756d70636170202857697265736861726b2920332e322e3320284769742076332e322e33207061636b6167656420617320332e322'
    'e332d3129000000000000b80000000100000058000000710000000000040002000300616e790009000100090000000b000e00007564702070'
    '6f7274203538343700000c0016004c696e757820352e382e302d35392d67656e6572696300000000000058000000060000007c02000000000'
    '0008c899316cad3b1a15b0200005b0200000003000100060242c0a83402000008004500024bb6aa4000401197a6c0a83402c0a834fe163716'
    'd70237ec996d61632d6c746501000302004a03000004041607010a000f00013a3e210221151f350000000004a00101480160eac1012202020'
    '64a8ed30000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '7c020000050000006c000000000000008fc70500026a6cc201001c00436f756e746572732070726f76696465642062792064756d706361700'
    '20008008fc705009b0ae9c0030008008fc70500fb696cc2040008003400000000000000050008000000000000000000000000006c000000'
)


def test_parsing_emm_identity_response_imsi(tmp_path):
    p = tmp_path / 'identity_response_imsi.pcap'
    p.write_bytes(bytes.fromhex(IDENTITY_RESPONSE_PCAP_DATA_IMSI))
    pcap = FileCapture(str(p))
    rar = EventsFactory().from_packet(list(pcap)[0])
    assert rar == {
        'imsi': '001010123456789',
        'event': IDENTITY_RESPONSE_NAME,
        'rnti': 74,
        'time': datetime.datetime(2021, 7, 20, 18, 32, 7, 512094),
    }
