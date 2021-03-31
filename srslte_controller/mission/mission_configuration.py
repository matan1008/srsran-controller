from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class GsmNeighbor:
    arfcn: int
    band: str


@dataclass
class MissionConfiguration:
    id: str = field(default_factory=lambda: str(uuid4()))
    mcc: str = '001'
    mnc: str = '01'
    mme_code: str = '0x1a'
    mme_group: str = '0x0001'
    tac: int = 0x0007
    apn: str = 'internet'
    gsm_neighbors: list[GsmNeighbor] = field(default_factory=list)
    cell_id: int = 0x01
    pci = 1
    earfcn = 3350
    device_name: str = 'zmq'
    device_args: str = ''
    enb_id: int = 0x19B

    @staticmethod
    def from_dict(data: dict):
        data['gsm_neighbors'] = [GsmNeighbor(**neighbor_data) for neighbor_data in data.get('gsm_neighbors', [])]
        return MissionConfiguration(**data)
