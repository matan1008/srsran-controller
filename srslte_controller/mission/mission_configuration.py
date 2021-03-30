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

    @staticmethod
    def from_dict(data: dict):
        data['gsm_neighbors'] = [GsmNeighbor(**neighbor_data) for neighbor_data in data.get('gsm_neighbors', [])]
        return MissionConfiguration(**data)
