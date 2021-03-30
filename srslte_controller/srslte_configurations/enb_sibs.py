from dataclasses import dataclass, asdict, field
from typing import TextIO

import libconf


@dataclass
class SrsEnbSib1SchedulerInfo:
    si_periodicity: int
    si_mapping_info: list[int]


@dataclass
class SrsEnbSib1:
    # When cell status "barred" is indicated, allow the UE to select another cell on the same frequency.
    intra_freq_reselection: str = 'Allowed'
    q_rx_lev_min: int = -70  # The lowest minimum available, equals to -140dB.
    # All UEs shall treat this cell as candidate during the cell selection and cell re-selection procedures.
    cell_barred: str = 'NotBarred'
    si_window_length: int = 20  # In ms.
    # By default, transmit only SIB2, SIB3 and SIB7.
    sched_info: tuple[SrsEnbSib1SchedulerInfo, ...] = field(
        default_factory=lambda: (SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3, 7]),)
    )
    system_info_value_tag: int = 0  # Indicates if a change has occurred in the SI messages


@dataclass
class SrsEnbSib2RrRach:
    num_ra_preambles: int = 64  # the highest number available for non-dedicated random access preambles.
    preamble_init_rx_target_pwr: int = -90  # The highest power for transmission of the initial preamble, in dBm.
    pwr_ramping_step: int = 6  # The biggest increase for PRACH retransmissions, in dB.
    preamble_trans_max: int = 200  # The maximum access attempts per UE.
    ra_resp_win_size: int = 10  # The longest timer to wait for RA response after RA preamble, in subframes.
    # The longest timer to wait for Contention Resolution message after sending Msg3, in subframes.
    mac_con_res_timer: int = 64
    # Higher value causes higher success rate of transmitting Msg3 and higher delay for retransmitting preambles.
    max_harq_msg3_tx: int = 4


@dataclass
class SrsEnbSib2RrBcch:
    modification_period_coeff: int


@dataclass
class SrsEnbSib2RrPcch:
    default_paging_cycle: int
    nB: str


@dataclass
class SrsEnbSib2RrPrachInfo:
    high_speed_flag: bool
    prach_config_index: int
    prach_freq_offset: int
    zero_correlation_zone_config: int


@dataclass
class SrsEnbSib2RrPrach:
    root_sequence_index: int
    prach_cnfg_info: SrsEnbSib2RrPrachInfo


@dataclass
class SrsEnbSib2RrPdsch:
    p_b: int
    rs_power: int


@dataclass
class SrsEnbSib2RrPuschUlRs:
    cyclic_shift: int
    group_assignment_pusch: int
    group_hopping_enabled: bool
    sequence_hopping_enabled: bool


@dataclass
class SrsEnbSib2RrPusch:
    n_sb: int
    hopping_mode: str
    pusch_hopping_offset: int
    enable_64_qam: bool
    ul_rs: SrsEnbSib2RrPuschUlRs


@dataclass
class SrsEnbSib2RrPucch:
    delta_pucch_shift: int
    n_rb_cqi: int
    n_cs_an: int
    n1_pucch_an: int


@dataclass
class SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch:
    format_1: int
    format_1b: int
    format_2: int
    format_2a: int
    format_2b: int


@dataclass
class SrsEnbSib2RrUlPwrCtrl:
    p0_nominal_pusch: int
    alpha: float
    p0_nominal_pucch: int
    delta_flist_pucch: SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch
    delta_preamble_msg3: int


@dataclass
class SrsEnbSib2Rr:
    rach_cnfg: SrsEnbSib2RrRach
    bcch_cnfg: SrsEnbSib2RrBcch
    pcch_cnfg: SrsEnbSib2RrPcch
    prach_cnfg: SrsEnbSib2RrPrach
    pdsch_cnfg: SrsEnbSib2RrPdsch
    pusch_cnfg: SrsEnbSib2RrPusch
    pucch_cnfg: SrsEnbSib2RrPucch
    ul_pwr_ctrl: SrsEnbSib2RrUlPwrCtrl
    ul_cp_length: str


@dataclass
class SrsEnbSib2UeTimersAndConstants:
    t300: int
    t301: int
    t310: int
    n310: int
    t311: int
    n311: int


@dataclass
class SrsEnbSib2FreqInfo:
    ul_carrier_freq_present: bool
    ul_bw_present: bool
    additional_spectrum_emission: int


@dataclass
class SrsEnbSib2:
    rr_config_common_sib: SrsEnbSib2Rr
    ue_timers_and_constants: SrsEnbSib2UeTimersAndConstants
    freqInfo: SrsEnbSib2FreqInfo
    time_alignment_timer: str


@dataclass
class SrsEnbSib3CellReselectionCommon:
    q_hyst: int


@dataclass
class SrsEnbSib3CellReselectionServing:
    s_non_intra_search: int
    thresh_serving_low: int
    cell_resel_prio: int


@dataclass
class SrsEnbSib3IntraFreqReselection:
    q_rx_lev_min: int
    p_max: int
    s_intra_search: int
    presence_ant_port_1: bool
    neigh_cell_cnfg: int
    t_resel_eutra: int


@dataclass
class SrsEnbSib3:
    cell_reselection_common: SrsEnbSib3CellReselectionCommon
    cell_reselection_serving: SrsEnbSib3CellReselectionServing
    intra_freq_reselection: SrsEnbSib3IntraFreqReselection


@dataclass
class SrsEnbSib7CarrierFreqsInfo:
    cell_resel_prio: int
    ncc_permitted: int
    q_rx_lev_min: int
    thresh_x_high: int
    thresh_x_low: int
    start_arfcn: int
    band_ind: str
    explicit_list_of_arfcns: tuple[int, ...]


@dataclass
class SrsEnbSib7:
    t_resel_geran: int
    carrier_freqs_info_list: tuple[SrsEnbSib7CarrierFreqsInfo, ...]


@dataclass
class SrsEnbSibs:
    sib1: SrsEnbSib1
    sib2: SrsEnbSib2
    sib3: SrsEnbSib3
    sib7: SrsEnbSib7

    def write(self, fd: TextIO):
        libconf.dump(asdict(self), fd)
