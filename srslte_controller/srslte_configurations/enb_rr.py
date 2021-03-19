from dataclasses import dataclass, asdict
from typing import TextIO

import libconf


@dataclass
class SrsEnbRRMacConfigPhr:
    dl_pathloss_change: str
    periodic_phr_timer: int
    prohibit_phr_timer: int


@dataclass
class SrsEnbRRMacConfigUlsch:
    max_harq_tx: int
    periodic_bsr_timer: int  # In ms.
    retx_bsr_timer: int  # In ms.


@dataclass
class SrsEnbRRMacConfig:
    phr_cnfg: SrsEnbRRMacConfigPhr
    ulsch_cnfg: SrsEnbRRMacConfigUlsch
    time_alignment_timer: int


@dataclass
class SrsEnbRRPhyConfigPhich:
    duration: str
    resources: str


@dataclass
class SrsEnbRRPhyConfigPuschDed:
    beta_offset_ack_idx: int
    beta_offset_ri_idx: int
    beta_offset_cqi_idx: int


@dataclass
class SrsEnbRRPhyConfigSchedRequest:
    dsr_trans_max: int
    period: int
    nof_prb: int


@dataclass
class SrsEnbRRPhyConfigCqiReport:
    mode: str
    simultaneousAckCQI: bool
    period: int
    nof_prb: int
    m_ri: int


@dataclass
class SrsEnbRRPhyConfig:
    phich_cnfg: SrsEnbRRPhyConfigPhich
    pusch_cnfg_ded: SrsEnbRRPhyConfigPuschDed
    sched_request_cnfg: SrsEnbRRPhyConfigSchedRequest
    cqi_report_cnfg: SrsEnbRRPhyConfigCqiReport


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
    a3_report_type: str
    a3_offset: int
    a3_hysteresis: int
    a3_time_to_trigger: int  # In ms.
    rsrq_config: int


@dataclass
class SrsEnbRRCell:
    cell_id: int
    tac: int
    pci: int
    dl_earfcn: int
    ho_active: bool
    scell_list: tuple[SrsEnbRRCellListScell, ...]
    meas_cell_list: tuple[SrsEnbRRCellListMeasCell, ...]
    meas_report_desc: SrsEnbRRCellListMeasReportDesc


@dataclass
class SrsEnbRR:
    mac_cnfg: SrsEnbRRMacConfig
    phy_cnfg: SrsEnbRRPhyConfig
    cell_list: tuple[SrsEnbRRCell, ...]

    def write(self, fd: TextIO):
        libconf.dump(asdict(self), fd)
