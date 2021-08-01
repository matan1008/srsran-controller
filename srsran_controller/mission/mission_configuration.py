from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class EnbCell:
    cell_id: int = 0x01
    pci: int = 1
    earfcn: int = 3350


@dataclass
class GsmNeighbor:
    arfcn: int
    band: str


@dataclass
class MissionConfiguration:
    id: str = field(default_factory=lambda: str(uuid4()))
    gsm_neighbors: list[GsmNeighbor] = field(default_factory=list)
    cells: list[EnbCell] = field(default_factory=lambda: [EnbCell()])
    name: str = 'New mission'
    mcc: str = '001'
    mnc: str = '01'
    mme_code: str = '0x1a'
    mme_group: str = '0x0001'
    tac: int = 0x0007
    apn: str = 'internet'
    device_name: str = 'zmq'
    device_args: str = ''
    enb_id: int = 0x19B
    full_net_name: str = 'Full network name'
    short_net_name: str = 'short'

    @staticmethod
    def from_dict(data: dict):
        data['gsm_neighbors'] = [GsmNeighbor(**neighbor_data) for neighbor_data in data.get('gsm_neighbors', [])]
        data['cells'] = [EnbCell(**cell_data) for cell_data in data.get('cells', [])]
        return MissionConfiguration(**data)
