import time

from pycrate_mobile.TS23040_SMS import *
from pycrate_mobile.TS24011_PPSMS import *

from srsran_controller.scripts.abstract import AbstractScript
from srsran_controller.uu_events.gsm_cp_ack import create as create_gsm_cp_ack
from srsran_controller.uu_events.gsm_rp_ack import create as create_gsm_rp_ack


def is_cp_ack(pkt):
    return bool(create_gsm_cp_ack(pkt))


def is_rp_ack(pkt):
    return bool(create_gsm_rp_ack(pkt))


class Sms(AbstractScript):
    def __init__(self, text: str, rp_oa: str, tp_oa: str):
        super().__init__()
        self.text = text
        self.rp_oa = rp_oa
        self.tp_oa = tp_oa

    def _construct_sms(self, rp_oa, tp_oa, text):
        deliver = SMS_DELIVER(val={
            'TP_MMS': 1,
            'TP_OA': {'Num': tp_oa, 'Type': 5, 'NumberingPlan': 8},
            'TP_DCS': {'Group': 1, 'Class': 1, 'Charset': 2},
            'TP_SCTS': (time.localtime(), time.altzone),
            'TP_UD': {'UD': text}
        })
        rp_data = RP_DATA_MT()
        rp_data.set_tpdu(deliver)
        rp_data['RPOriginatorAddress'].set_IE(val={'Num': rp_oa})
        cp_data = CP_DATA()
        cp_data.set_rp(rp_data)
        return cp_data.to_bytes()

    async def run(self):
        await self.ecm_connect()
        cp_data = self._construct_sms(self.rp_oa, self.tp_oa, self.text)
        self.log(f'Sending downlink nas transport {cp_data.hex()}')
        await self.mission.epc.send_downlink_nas_transport(self.imsi, cp_data)
        packet = await self.wait_for_parsed_packet(is_cp_ack)
        self.log('CP-ACK Received')
        # CP-ACK and RP-ACK might be sent in the same packet.
        if not is_rp_ack(packet):
            await self.wait_for_parsed_packet(is_rp_ack)
        self.log('RP-ACK Received')
        cp_ack = CP_ACK()
        self.log(f'Sending downlink nas transport {cp_ack.to_bytes().hex()}')
        await self.mission.epc.send_downlink_nas_transport(self.imsi, cp_ack.to_bytes())
