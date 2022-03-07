from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class EnbCell:
    cell_id: int = 0x01
    pci: int = 1
    earfcn: int = 3350


@dataclass
class IntraFreqNeighbour:
    phys_cell_id: int
    q_offset_cell: int


@dataclass
class GsmNeighbour:
    arfcn: int
    band: str


@dataclass
class MissionConfiguration:
    id: str = field(default_factory=lambda: str(uuid4()))
    intra_freq_neighbours: list[IntraFreqNeighbour] = field(default_factory=list)
    gsm_neighbours: list[GsmNeighbour] = field(default_factory=list)
    cells: list[EnbCell] = field(default_factory=lambda: [EnbCell()])
    name: str = 'New mission'
    mcc: str = '001'
    mnc: str = '01'
    mme_code: str = '0x1a'
    mme_group: str = '0x0001'
    tac: int = 0x0007
    apn: str = 'internet'
    device_name: str = 'UHD'
    device_args: str = 'clock=gpsdo'
    enb_id: int = 0x19B
    full_net_name: str = 'Full network name'
    short_net_name: str = 'short'
    external_interface: str = 'none'

    @staticmethod
    def from_dict(data: dict):
        data['intra_freq_neighbours'] = [IntraFreqNeighbour(**neigh) for neigh in data.get('intra_freq_neighbours', [])]
        data['gsm_neighbours'] = [GsmNeighbour(**neigh) for neigh in data.get('gsm_neighbours', [])]
        data['cells'] = [EnbCell(**cell_data) for cell_data in data.get('cells', [])]
        return MissionConfiguration(**data)
