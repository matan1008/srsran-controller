from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class MissionConfiguration:
    id: str = field(default_factory=lambda: str(uuid4()))
    mcc: str = '001'
    mnc: str = '01'
