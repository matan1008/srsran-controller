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
    modification_period_coeff: int = 2  # Make the modification period as small as possible.


@dataclass
class SrsEnbSib2RrPcch:
    default_paging_cycle: int = 32  # Smaller value leads to lower latency but higher battery consumption.
    nB: str = '1'


@dataclass
class SrsEnbSib2RrPrachInfo:
    high_speed_flag: bool = False
    prach_config_index: int = 3
    prach_freq_offset: int = 2
    zero_correlation_zone_config: int = 5


@dataclass
class SrsEnbSib2RrPrach:
    root_sequence_index: int = 128
    prach_cnfg_info: SrsEnbSib2RrPrachInfo = field(default_factory=SrsEnbSib2RrPrachInfo)


@dataclass
class SrsEnbSib2RrPdsch:
    p_b: int = 1
    rs_power: int = 0


@dataclass
class SrsEnbSib2RrPuschUlRs:
    cyclic_shift: int = 0
    group_assignment_pusch: int = 0
    group_hopping_enabled: bool = False
    sequence_hopping_enabled: bool = False


@dataclass
class SrsEnbSib2RrPusch:
    n_sb: int = 1
    hopping_mode: str = 'inter-subframe'
    pusch_hopping_offset: int = 2
    enable_64_qam: bool = False
    ul_rs: SrsEnbSib2RrPuschUlRs = field(default_factory=SrsEnbSib2RrPuschUlRs)


@dataclass
class SrsEnbSib2RrPucch:
    delta_pucch_shift: int = 2
    n_rb_cqi: int = 2
    n_cs_an: int = 0
    n1_pucch_an: int = 12


@dataclass
class SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch:
    format_1: int = 0
    format_1b: int = 3
    format_2: int = 1
    format_2a: int = 2
    format_2b: int = 2


@dataclass
class SrsEnbSib2RrUlPwrCtrl:
    p0_nominal_pusch: int = 24  # The highest expected arrival power of PUSCH, in dBm.
    alpha: float = 0.7
    p0_nominal_pucch: int = -96  # The highest expected arrival power of PUCCH, in dBm.
    delta_flist_pucch: SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch = field(
        default_factory=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch
    )
    delta_preamble_msg3: int = 6


@dataclass
class SrsEnbSib2Rr:
    rach_cnfg: SrsEnbSib2RrRach = field(default_factory=SrsEnbSib2RrRach)
    bcch_cnfg: SrsEnbSib2RrBcch = field(default_factory=SrsEnbSib2RrBcch)
    pcch_cnfg: SrsEnbSib2RrPcch = field(default_factory=SrsEnbSib2RrPcch)
    prach_cnfg: SrsEnbSib2RrPrach = field(default_factory=SrsEnbSib2RrPrach)
    pdsch_cnfg: SrsEnbSib2RrPdsch = field(default_factory=SrsEnbSib2RrPdsch)
    pusch_cnfg: SrsEnbSib2RrPusch = field(default_factory=SrsEnbSib2RrPusch)
    pucch_cnfg: SrsEnbSib2RrPucch = field(default_factory=SrsEnbSib2RrPucch)
    ul_pwr_ctrl: SrsEnbSib2RrUlPwrCtrl = field(default_factory=SrsEnbSib2RrUlPwrCtrl)
    ul_cp_length: str = 'len1'


@dataclass
class SrsEnbSib2UeTimersAndConstants:
    t300: int = 2000
    t301: int = 100
    t310: int = 200
    n310: int = 1
    t311: int = 10000
    n311: int = 1


@dataclass
class SrsEnbSib2FreqInfo:
    ul_carrier_freq_present: bool = True
    ul_bw_present: bool = True
    additional_spectrum_emission: int = 1


@dataclass
class SrsEnbSib2:
    rr_config_common_sib: SrsEnbSib2Rr = field(default_factory=SrsEnbSib2Rr)
    ue_timers_and_constants: SrsEnbSib2UeTimersAndConstants = field(default_factory=SrsEnbSib2UeTimersAndConstants)
    freqInfo: SrsEnbSib2FreqInfo = field(default_factory=SrsEnbSib2FreqInfo)
    time_alignment_timer: str = 'INFINITY'


@dataclass
class SrsEnbSib3CellReselectionCommon:
    q_hyst: int = 24  # Higher hysteresis helps the serving cell when ranking against neighboring cells, in dB.


@dataclass
class SrsEnbSib3CellReselectionServing:
    # Lower value prevents UE from performing measurements on cells of equal or lower priority.
    s_non_intra_search: int = 0
    # Lower value prevents UE from performing cell reselection to a cell with lower priority.
    thresh_serving_low: int = 0
    cell_resel_prio: int = 7  # UEs perform measurements on higher priority cells


@dataclass
class SrsEnbSib3IntraFreqReselection:
    q_rx_lev_min: int = -70  # Lower value will result in higher Selection Criterion, actual value multiplied by 2 dBm.
    p_max: int = 23
    s_intra_search: int = 0  # Lower value prevents UE from performing intra-frequency measurements.
    presence_ant_port_1: bool = True
    neigh_cell_cnfg: int = 1  # No MBSFN subframes are present in all neighbour cells
    t_resel_eutra: int = 1


@dataclass
class SrsEnbSib3:
    cell_reselection_common: SrsEnbSib3CellReselectionCommon = field(default_factory=SrsEnbSib3CellReselectionCommon)
    cell_reselection_serving: SrsEnbSib3CellReselectionServing = field(default_factory=SrsEnbSib3CellReselectionServing)
    intra_freq_reselection: SrsEnbSib3IntraFreqReselection = field(default_factory=SrsEnbSib3IntraFreqReselection)


@dataclass
class SrsEnbSib7CarrierFreqsInfo:
    cell_resel_prio: int = 7
    ncc_permitted: int = 255  # Allow all UEs to monitor this frequency.
    q_rx_lev_min: int = 0  # Lower value will ease selection, actual value is (value * 2) - 115 dBm.
    # Lower value allows UE to select this frequency when the priority of this frequency is higher.
    thresh_x_high: int = 0
    # Lower value allows UE to select this frequency when the priority of this frequency is lower.
    thresh_x_low: int = 0
    start_arfcn: int = 871
    band_ind: str = 'dcs1800'
    explicit_list_of_arfcns: tuple[int, ...] = field(default_factory=lambda: (871,))


@dataclass
class SrsEnbSib7:
    t_resel_geran: int = 1
    carrier_freqs_info_list: tuple[SrsEnbSib7CarrierFreqsInfo, ...] = field(default_factory=tuple)


@dataclass
class SrsEnbSibs:
    sib1: SrsEnbSib1 = field(default_factory=SrsEnbSib1)
    sib2: SrsEnbSib2 = field(default_factory=SrsEnbSib2)
    sib3: SrsEnbSib3 = field(default_factory=SrsEnbSib3)
    sib7: SrsEnbSib7 = field(default_factory=SrsEnbSib7)

    def write(self, fd: TextIO):
        libconf.dump(asdict(self), fd)
