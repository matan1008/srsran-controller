from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class MissionConfiguration:
    id: str = field(default_factory=lambda: str(uuid4()))
    mcc: str = '001'
    mnc: str = '01'
    mme_code: str = '0x1a'
    mme_group: str = '0x0001'
    tac: int = 0x0007
    apn: str = 'internet'
