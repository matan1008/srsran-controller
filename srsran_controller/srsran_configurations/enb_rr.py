from dataclasses import dataclass, asdict, field
from typing import TextIO

import libconf

__all__ = [
    'SrsEnbRRMacConfigPhr', 'SrsEnbRRMacConfigUlsch', 'SrsEnbRRMacConfig', 'SrsEnbRRPhyConfigPhich',
    'SrsEnbRRPhyConfigPuschDed', 'SrsEnbRRPhyConfigSchedRequest', 'SrsEnbRRPhyConfigCqiReport', 'SrsEnbRRPhyConfig',
    'SrsEnbRRCellListScell', 'SrsEnbRRCellListMeasCell', 'SrsEnbRRCellListMeasReportDesc', 'SrsEnbRRCell', 'SrsEnbRR'
]


@dataclass
class SrsEnbRRMacConfigPhr:
    dl_pathloss_change: str = 'dB1'  # Each change in the pathloss will trigger power headroom reporting.
    periodic_phr_timer: int = 50  # In subframes.
    prohibit_phr_timer: int = 0  # Don't delay between pathloss changes, in subframes.


@dataclass
class SrsEnbRRMacConfigUlsch:
    max_harq_tx: int = 28  # Higher value allows more HARQ retransmissions.
    periodic_bsr_timer: int = 64  # Lower value yields more reports, in subframes.
    retx_bsr_timer: int = 320  # Lower value yields more reports, in subframes.


@dataclass
class SrsEnbRRMacConfig:
    phr_cnfg: SrsEnbRRMacConfigPhr = field(default_factory=SrsEnbRRMacConfigPhr)
    ulsch_cnfg: SrsEnbRRMacConfigUlsch = field(default_factory=SrsEnbRRMacConfigUlsch)
    # Lower value will cause the UE to invalidate time advance more often, in subframes.
    time_alignment_timer: int = 500


@dataclass
class SrsEnbRRPhyConfigPhich:
    duration: str = 'Normal'
    resources: str = '1/6'


@dataclass
class SrsEnbRRPhyConfigPuschDed:
    beta_offset_ack_idx: int = 6
    beta_offset_ri_idx: int = 6
    beta_offset_cqi_idx: int = 6


@dataclass
class SrsEnbRRPhyConfigSchedRequest:
    dsr_trans_max: int = 64  # Allow as many Scheduling Request tries as possible.
    period: int = 20
    nof_prb: int = 2


@dataclass
class SrsEnbRRPhyConfigCqiReport:
    mode: str = 'periodic'
    simultaneousAckCQI: bool = True
    period: int = 40
    nof_prb: int = 2
    m_ri: int = 8


@dataclass
class SrsEnbRRPhyConfig:
    phich_cnfg: SrsEnbRRPhyConfigPhich = field(default_factory=SrsEnbRRPhyConfigPhich)
    pusch_cnfg_ded: SrsEnbRRPhyConfigPuschDed = field(default_factory=SrsEnbRRPhyConfigPuschDed)
    sched_request_cnfg: SrsEnbRRPhyConfigSchedRequest = field(default_factory=SrsEnbRRPhyConfigSchedRequest)
    cqi_report_cnfg: SrsEnbRRPhyConfigCqiReport = field(default_factory=SrsEnbRRPhyConfigCqiReport)


@dataclass
class SrsEnbRRCellListScell:
    cell_id: str
    cross_carrier_scheduling: bool
    scheduling_cell_id: str
    ul_allowed: bool


@dataclass
class SrsEnbRRCellListMeasCell:
    eci: int
    dl_earfcn: int
    pci: int


@dataclass
class SrsEnbRRCellListMeasReportDesc:
    a3_report_type: str = 'RSRP'
    a3_offset: int = 6
    a3_hysteresis: int = 0
    a3_time_to_trigger: int = 480  # In ms.
    rsrq_config: int = 4


@dataclass
class SrsEnbRRCell:
    cell_id: int
    tac: int
    pci: int
    dl_earfcn: int
    rf_port: int = 0
    ho_active: bool = False
    tx_gain: float = 20.0
    scell_list: tuple[SrsEnbRRCellListScell, ...] = field(default_factory=tuple)
    meas_cell_list: tuple[SrsEnbRRCellListMeasCell, ...] = field(default_factory=tuple)
    meas_report_desc: SrsEnbRRCellListMeasReportDesc = field(default_factory=SrsEnbRRCellListMeasReportDesc)


@dataclass
class SrsEnbRR:
    mac_cnfg: SrsEnbRRMacConfig = field(default_factory=SrsEnbRRMacConfig)
    phy_cnfg: SrsEnbRRPhyConfig = field(default_factory=SrsEnbRRPhyConfig)
    cell_list: tuple[SrsEnbRRCell, ...] = field(default_factory=tuple)

    def write(self, fd: TextIO):
        libconf.dump(asdict(self), fd)
