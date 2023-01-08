from io import StringIO

from srsran_controller.srsran_configurations.enb_sibs import *


def test_sanity():
    output = StringIO()
    SrsEnbSibs(
        SrsEnbSib1(intra_freq_reselection='Allowed', q_rx_lev_min=-65, cell_barred='NotBarred', si_window_length=20,
                   sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3]),),
                   system_info_value_tag=0),
        SrsEnbSib2(
            rr_config_common_sib=SrsEnbSib2Rr(
                rach_cnfg=SrsEnbSib2RrRach(num_ra_preambles=52, preamble_init_rx_target_pwr=-104, pwr_ramping_step=6,
                                           preamble_trans_max=10, ra_resp_win_size=10, mac_con_res_timer=64,
                                           max_harq_msg3_tx=4),
                bcch_cnfg=SrsEnbSib2RrBcch(modification_period_coeff=16),
                pcch_cnfg=SrsEnbSib2RrPcch(default_paging_cycle=32, nB='1'),
                prach_cnfg=SrsEnbSib2RrPrach(
                    root_sequence_index=128,
                    prach_cnfg_info=SrsEnbSib2RrPrachInfo(high_speed_flag=False, prach_config_index=3,
                                                          prach_freq_offset=2,
                                                          zero_correlation_zone_config=5)
                ),
                pdsch_cnfg=SrsEnbSib2RrPdsch(p_b=1, rs_power=0),
                pusch_cnfg=SrsEnbSib2RrPusch(
                    n_sb=1, hopping_mode='inter-subframe', pusch_hopping_offset=2, enable_64_qam=False,
                    ul_rs=SrsEnbSib2RrPuschUlRs(cyclic_shift=0, group_assignment_pusch=0, group_hopping_enabled=False,
                                                sequence_hopping_enabled=False)
                ),
                pucch_cnfg=SrsEnbSib2RrPucch(delta_pucch_shift=2, n_rb_cqi=2, n_cs_an=0, n1_pucch_an=12),
                ul_pwr_ctrl=SrsEnbSib2RrUlPwrCtrl(
                    p0_nominal_pusch=-85, alpha=0.7, p0_nominal_pucch=-107, delta_preamble_msg3=6,
                    delta_flist_pucch=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch(
                        format_1=0, format_1b=3, format_2=1, format_2a=2, format_2b=2
                    )
                ),
                ul_cp_length='len1'
            ),
            ue_timers_and_constants=SrsEnbSib2UeTimersAndConstants(t300=2000, t301=100, t310=200, n310=1, t311=10000,
                                                                   n311=1),
            freqInfo=SrsEnbSib2FreqInfo(ul_carrier_freq_present=True, ul_bw_present=True,
                                        additional_spectrum_emission=1),
            time_alignment_timer='INFINITY'
        ),
        SrsEnbSib3(
            cell_reselection_common=SrsEnbSib3CellReselectionCommon(q_hyst=2),
            cell_reselection_serving=SrsEnbSib3CellReselectionServing(s_non_intra_search=3, thresh_serving_low=2,
                                                                      cell_resel_prio=6),
            intra_freq_reselection=SrsEnbSib3IntraFreqReselection(q_rx_lev_min=-61, p_max=23, s_intra_search=5,
                                                                  presence_ant_port_1=True, neigh_cell_cnfg=1,
                                                                  t_resel_eutra=1)
        ),
    ).write(output)
    assert output.getvalue() == (
        'sib1 =\n'
        '{\n'
        '    intra_freq_reselection = "Allowed";\n'
        '    q_rx_lev_min = -65;\n'
        '    cell_barred = "NotBarred";\n'
        '    si_window_length = 20;\n'
        '    sched_info =\n'
        '    (\n'
        '        {\n'
        '            si_periodicity = 16;\n'
        '            si_mapping_info =\n'
        '            [\n'
        '                3\n'
        '            ];\n'
        '        }\n'
        '    );\n'
        '    system_info_value_tag = 0;\n'
        '};\n'
        'sib2 =\n'
        '{\n'
        '    rr_config_common_sib =\n'
        '    {\n'
        '        rach_cnfg =\n'
        '        {\n'
        '            num_ra_preambles = 52;\n'
        '            preamble_init_rx_target_pwr = -104;\n'
        '            pwr_ramping_step = 6;\n'
        '            preamble_trans_max = 10;\n'
        '            ra_resp_win_size = 10;\n'
        '            mac_con_res_timer = 64;\n'
        '            max_harq_msg3_tx = 4;\n'
        '        };\n'
        '        bcch_cnfg =\n'
        '        {\n'
        '            modification_period_coeff = 16;\n'
        '        };\n'
        '        pcch_cnfg =\n'
        '        {\n'
        '            default_paging_cycle = 32;\n'
        '            nB = "1";\n'
        '        };\n'
        '        prach_cnfg =\n'
        '        {\n'
        '            root_sequence_index = 128;\n'
        '            prach_cnfg_info =\n'
        '            {\n'
        '                high_speed_flag = False;\n'
        '                prach_config_index = 3;\n'
        '                prach_freq_offset = 2;\n'
        '                zero_correlation_zone_config = 5;\n'
        '            };\n'
        '        };\n'
        '        pdsch_cnfg =\n'
        '        {\n'
        '            p_b = 1;\n'
        '            rs_power = 0;\n'
        '        };\n'
        '        pusch_cnfg =\n'
        '        {\n'
        '            n_sb = 1;\n'
        '            hopping_mode = "inter-subframe";\n'
        '            pusch_hopping_offset = 2;\n'
        '            enable_64_qam = False;\n'
        '            ul_rs =\n'
        '            {\n'
        '                cyclic_shift = 0;\n'
        '                group_assignment_pusch = 0;\n'
        '                group_hopping_enabled = False;\n'
        '                sequence_hopping_enabled = False;\n'
        '            };\n'
        '        };\n'
        '        pucch_cnfg =\n'
        '        {\n'
        '            delta_pucch_shift = 2;\n'
        '            n_rb_cqi = 2;\n'
        '            n_cs_an = 0;\n'
        '            n1_pucch_an = 12;\n'
        '        };\n'
        '        ul_pwr_ctrl =\n'
        '        {\n'
        '            p0_nominal_pusch = -85;\n'
        '            alpha = 0.7;\n'
        '            p0_nominal_pucch = -107;\n'
        '            delta_flist_pucch =\n'
        '            {\n'
        '                format_1 = 0;\n'
        '                format_1b = 3;\n'
        '                format_2 = 1;\n'
        '                format_2a = 2;\n'
        '                format_2b = 2;\n'
        '            };\n'
        '            delta_preamble_msg3 = 6;\n'
        '        };\n'
        '        ul_cp_length = "len1";\n'
        '    };\n'
        '    ue_timers_and_constants =\n'
        '    {\n'
        '        t300 = 2000;\n'
        '        t301 = 100;\n'
        '        t310 = 200;\n'
        '        n310 = 1;\n'
        '        t311 = 10000;\n'
        '        n311 = 1;\n'
        '    };\n'
        '    freqInfo =\n'
        '    {\n'
        '        ul_carrier_freq_present = True;\n'
        '        ul_bw_present = True;\n'
        '        additional_spectrum_emission = 1;\n'
        '    };\n'
        '    time_alignment_timer = "INFINITY";\n'
        '};\n'
        'sib3 =\n'
        '{\n'
        '    cell_reselection_common =\n'
        '    {\n'
        '        q_hyst = 2;\n'
        '    };\n'
        '    cell_reselection_serving =\n'
        '    {\n'
        '        s_non_intra_search = 3;\n'
        '        thresh_serving_low = 2;\n'
        '        cell_resel_prio = 6;\n'
        '    };\n'
        '    intra_freq_reselection =\n'
        '    {\n'
        '        q_rx_lev_min = -61;\n'
        '        p_max = 23;\n'
        '        s_intra_search = 5;\n'
        '        presence_ant_port_1 = True;\n'
        '        neigh_cell_cnfg = 1;\n'
        '        t_resel_eutra = 1;\n'
        '    };\n'
        '};\n'
    )


def test_sib4():
    output = StringIO()
    SrsEnbSibs(
        SrsEnbSib1(intra_freq_reselection='Allowed', q_rx_lev_min=-65, cell_barred='NotBarred', si_window_length=20,
                   sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3, 4]),),
                   system_info_value_tag=0),
        SrsEnbSib2(
            rr_config_common_sib=SrsEnbSib2Rr(
                rach_cnfg=SrsEnbSib2RrRach(num_ra_preambles=52, preamble_init_rx_target_pwr=-104, pwr_ramping_step=6,
                                           preamble_trans_max=10, ra_resp_win_size=10, mac_con_res_timer=64,
                                           max_harq_msg3_tx=4),
                bcch_cnfg=SrsEnbSib2RrBcch(modification_period_coeff=16),
                pcch_cnfg=SrsEnbSib2RrPcch(default_paging_cycle=32, nB='1'),
                prach_cnfg=SrsEnbSib2RrPrach(
                    root_sequence_index=128,
                    prach_cnfg_info=SrsEnbSib2RrPrachInfo(high_speed_flag=False, prach_config_index=3,
                                                          prach_freq_offset=2,
                                                          zero_correlation_zone_config=5)
                ),
                pdsch_cnfg=SrsEnbSib2RrPdsch(p_b=1, rs_power=0),
                pusch_cnfg=SrsEnbSib2RrPusch(
                    n_sb=1, hopping_mode='inter-subframe', pusch_hopping_offset=2, enable_64_qam=False,
                    ul_rs=SrsEnbSib2RrPuschUlRs(cyclic_shift=0, group_assignment_pusch=0, group_hopping_enabled=False,
                                                sequence_hopping_enabled=False)
                ),
                pucch_cnfg=SrsEnbSib2RrPucch(delta_pucch_shift=2, n_rb_cqi=2, n_cs_an=0, n1_pucch_an=12),
                ul_pwr_ctrl=SrsEnbSib2RrUlPwrCtrl(
                    p0_nominal_pusch=-85, alpha=0.7, p0_nominal_pucch=-107, delta_preamble_msg3=6,
                    delta_flist_pucch=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch(
                        format_1=0, format_1b=3, format_2=1, format_2a=2, format_2b=2
                    )
                ),
                ul_cp_length='len1'
            ),
            ue_timers_and_constants=SrsEnbSib2UeTimersAndConstants(t300=2000, t301=100, t310=200, n310=1, t311=10000,
                                                                   n311=1),
            freqInfo=SrsEnbSib2FreqInfo(ul_carrier_freq_present=True, ul_bw_present=True,
                                        additional_spectrum_emission=1),
            time_alignment_timer='INFINITY'
        ),
        SrsEnbSib3(
            cell_reselection_common=SrsEnbSib3CellReselectionCommon(q_hyst=2),
            cell_reselection_serving=SrsEnbSib3CellReselectionServing(s_non_intra_search=3, thresh_serving_low=2,
                                                                      cell_resel_prio=6),
            intra_freq_reselection=SrsEnbSib3IntraFreqReselection(q_rx_lev_min=-61, p_max=23, s_intra_search=5,
                                                                  presence_ant_port_1=True, neigh_cell_cnfg=1,
                                                                  t_resel_eutra=1)
        ),
        sib4=SrsEnbSib4(
            intra_freq_neigh_cell_list=(SrsEnbSib4IntraFreqNeighCellInfo(phys_cell_id=3),),
            intra_freq_black_cell_list=(SrsEnbPhysCellIdRange(start=4, range=8),),
            csg_phys_cell_id_range=SrsEnbPhysCellIdRange(start=90, range=16),
        ),
    ).write(output)
    assert output.getvalue() == (
        'sib1 =\n'
        '{\n'
        '    intra_freq_reselection = "Allowed";\n'
        '    q_rx_lev_min = -65;\n'
        '    cell_barred = "NotBarred";\n'
        '    si_window_length = 20;\n'
        '    sched_info =\n'
        '    (\n'
        '        {\n'
        '            si_periodicity = 16;\n'
        '            si_mapping_info =\n'
        '            [\n'
        '                3,\n'
        '                4\n'
        '            ];\n'
        '        }\n'
        '    );\n'
        '    system_info_value_tag = 0;\n'
        '};\n'
        'sib2 =\n'
        '{\n'
        '    rr_config_common_sib =\n'
        '    {\n'
        '        rach_cnfg =\n'
        '        {\n'
        '            num_ra_preambles = 52;\n'
        '            preamble_init_rx_target_pwr = -104;\n'
        '            pwr_ramping_step = 6;\n'
        '            preamble_trans_max = 10;\n'
        '            ra_resp_win_size = 10;\n'
        '            mac_con_res_timer = 64;\n'
        '            max_harq_msg3_tx = 4;\n'
        '        };\n'
        '        bcch_cnfg =\n'
        '        {\n'
        '            modification_period_coeff = 16;\n'
        '        };\n'
        '        pcch_cnfg =\n'
        '        {\n'
        '            default_paging_cycle = 32;\n'
        '            nB = "1";\n'
        '        };\n'
        '        prach_cnfg =\n'
        '        {\n'
        '            root_sequence_index = 128;\n'
        '            prach_cnfg_info =\n'
        '            {\n'
        '                high_speed_flag = False;\n'
        '                prach_config_index = 3;\n'
        '                prach_freq_offset = 2;\n'
        '                zero_correlation_zone_config = 5;\n'
        '            };\n'
        '        };\n'
        '        pdsch_cnfg =\n'
        '        {\n'
        '            p_b = 1;\n'
        '            rs_power = 0;\n'
        '        };\n'
        '        pusch_cnfg =\n'
        '        {\n'
        '            n_sb = 1;\n'
        '            hopping_mode = "inter-subframe";\n'
        '            pusch_hopping_offset = 2;\n'
        '            enable_64_qam = False;\n'
        '            ul_rs =\n'
        '            {\n'
        '                cyclic_shift = 0;\n'
        '                group_assignment_pusch = 0;\n'
        '                group_hopping_enabled = False;\n'
        '                sequence_hopping_enabled = False;\n'
        '            };\n'
        '        };\n'
        '        pucch_cnfg =\n'
        '        {\n'
        '            delta_pucch_shift = 2;\n'
        '            n_rb_cqi = 2;\n'
        '            n_cs_an = 0;\n'
        '            n1_pucch_an = 12;\n'
        '        };\n'
        '        ul_pwr_ctrl =\n'
        '        {\n'
        '            p0_nominal_pusch = -85;\n'
        '            alpha = 0.7;\n'
        '            p0_nominal_pucch = -107;\n'
        '            delta_flist_pucch =\n'
        '            {\n'
        '                format_1 = 0;\n'
        '                format_1b = 3;\n'
        '                format_2 = 1;\n'
        '                format_2a = 2;\n'
        '                format_2b = 2;\n'
        '            };\n'
        '            delta_preamble_msg3 = 6;\n'
        '        };\n'
        '        ul_cp_length = "len1";\n'
        '    };\n'
        '    ue_timers_and_constants =\n'
        '    {\n'
        '        t300 = 2000;\n'
        '        t301 = 100;\n'
        '        t310 = 200;\n'
        '        n310 = 1;\n'
        '        t311 = 10000;\n'
        '        n311 = 1;\n'
        '    };\n'
        '    freqInfo =\n'
        '    {\n'
        '        ul_carrier_freq_present = True;\n'
        '        ul_bw_present = True;\n'
        '        additional_spectrum_emission = 1;\n'
        '    };\n'
        '    time_alignment_timer = "INFINITY";\n'
        '};\n'
        'sib3 =\n'
        '{\n'
        '    cell_reselection_common =\n'
        '    {\n'
        '        q_hyst = 2;\n'
        '    };\n'
        '    cell_reselection_serving =\n'
        '    {\n'
        '        s_non_intra_search = 3;\n'
        '        thresh_serving_low = 2;\n'
        '        cell_resel_prio = 6;\n'
        '    };\n'
        '    intra_freq_reselection =\n'
        '    {\n'
        '        q_rx_lev_min = -61;\n'
        '        p_max = 23;\n'
        '        s_intra_search = 5;\n'
        '        presence_ant_port_1 = True;\n'
        '        neigh_cell_cnfg = 1;\n'
        '        t_resel_eutra = 1;\n'
        '    };\n'
        '};\n'
        'sib4 =\n'
        '{\n'
        '    intra_freq_neigh_cell_list =\n'
        '    (\n'
        '        {\n'
        '            phys_cell_id = 3;\n'
        '            q_offset_range = 24;\n'
        '        }\n'
        '    );\n'
        '    intra_freq_black_cell_list =\n'
        '    (\n'
        '        {\n'
        '            start = 4;\n'
        '            range = 8;\n'
        '        }\n'
        '    );\n'
        '    csg_phys_cell_id_range =\n'
        '    {\n'
        '        start = 90;\n'
        '        range = 16;\n'
        '    };\n'
        '};\n'
    )


def test_sib4_minimal():
    output = StringIO()
    SrsEnbSibs(
        SrsEnbSib1(intra_freq_reselection='Allowed', q_rx_lev_min=-65, cell_barred='NotBarred', si_window_length=20,
                   sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3, 4]),),
                   system_info_value_tag=0),
        SrsEnbSib2(
            rr_config_common_sib=SrsEnbSib2Rr(
                rach_cnfg=SrsEnbSib2RrRach(num_ra_preambles=52, preamble_init_rx_target_pwr=-104, pwr_ramping_step=6,
                                           preamble_trans_max=10, ra_resp_win_size=10, mac_con_res_timer=64,
                                           max_harq_msg3_tx=4),
                bcch_cnfg=SrsEnbSib2RrBcch(modification_period_coeff=16),
                pcch_cnfg=SrsEnbSib2RrPcch(default_paging_cycle=32, nB='1'),
                prach_cnfg=SrsEnbSib2RrPrach(
                    root_sequence_index=128,
                    prach_cnfg_info=SrsEnbSib2RrPrachInfo(high_speed_flag=False, prach_config_index=3,
                                                          prach_freq_offset=2,
                                                          zero_correlation_zone_config=5)
                ),
                pdsch_cnfg=SrsEnbSib2RrPdsch(p_b=1, rs_power=0),
                pusch_cnfg=SrsEnbSib2RrPusch(
                    n_sb=1, hopping_mode='inter-subframe', pusch_hopping_offset=2, enable_64_qam=False,
                    ul_rs=SrsEnbSib2RrPuschUlRs(cyclic_shift=0, group_assignment_pusch=0, group_hopping_enabled=False,
                                                sequence_hopping_enabled=False)
                ),
                pucch_cnfg=SrsEnbSib2RrPucch(delta_pucch_shift=2, n_rb_cqi=2, n_cs_an=0, n1_pucch_an=12),
                ul_pwr_ctrl=SrsEnbSib2RrUlPwrCtrl(
                    p0_nominal_pusch=-85, alpha=0.7, p0_nominal_pucch=-107, delta_preamble_msg3=6,
                    delta_flist_pucch=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch(
                        format_1=0, format_1b=3, format_2=1, format_2a=2, format_2b=2
                    )
                ),
                ul_cp_length='len1'
            ),
            ue_timers_and_constants=SrsEnbSib2UeTimersAndConstants(t300=2000, t301=100, t310=200, n310=1, t311=10000,
                                                                   n311=1),
            freqInfo=SrsEnbSib2FreqInfo(ul_carrier_freq_present=True, ul_bw_present=True,
                                        additional_spectrum_emission=1),
            time_alignment_timer='INFINITY'
        ),
        SrsEnbSib3(
            cell_reselection_common=SrsEnbSib3CellReselectionCommon(q_hyst=2),
            cell_reselection_serving=SrsEnbSib3CellReselectionServing(s_non_intra_search=3, thresh_serving_low=2,
                                                                      cell_resel_prio=6),
            intra_freq_reselection=SrsEnbSib3IntraFreqReselection(q_rx_lev_min=-61, p_max=23, s_intra_search=5,
                                                                  presence_ant_port_1=True, neigh_cell_cnfg=1,
                                                                  t_resel_eutra=1)
        ),
        sib4=SrsEnbSib4(
            intra_freq_neigh_cell_list=(SrsEnbSib4IntraFreqNeighCellInfo(phys_cell_id=3),),
        ),
    ).write(output)
    assert output.getvalue() == (
        'sib1 =\n'
        '{\n'
        '    intra_freq_reselection = "Allowed";\n'
        '    q_rx_lev_min = -65;\n'
        '    cell_barred = "NotBarred";\n'
        '    si_window_length = 20;\n'
        '    sched_info =\n'
        '    (\n'
        '        {\n'
        '            si_periodicity = 16;\n'
        '            si_mapping_info =\n'
        '            [\n'
        '                3,\n'
        '                4\n'
        '            ];\n'
        '        }\n'
        '    );\n'
        '    system_info_value_tag = 0;\n'
        '};\n'
        'sib2 =\n'
        '{\n'
        '    rr_config_common_sib =\n'
        '    {\n'
        '        rach_cnfg =\n'
        '        {\n'
        '            num_ra_preambles = 52;\n'
        '            preamble_init_rx_target_pwr = -104;\n'
        '            pwr_ramping_step = 6;\n'
        '            preamble_trans_max = 10;\n'
        '            ra_resp_win_size = 10;\n'
        '            mac_con_res_timer = 64;\n'
        '            max_harq_msg3_tx = 4;\n'
        '        };\n'
        '        bcch_cnfg =\n'
        '        {\n'
        '            modification_period_coeff = 16;\n'
        '        };\n'
        '        pcch_cnfg =\n'
        '        {\n'
        '            default_paging_cycle = 32;\n'
        '            nB = "1";\n'
        '        };\n'
        '        prach_cnfg =\n'
        '        {\n'
        '            root_sequence_index = 128;\n'
        '            prach_cnfg_info =\n'
        '            {\n'
        '                high_speed_flag = False;\n'
        '                prach_config_index = 3;\n'
        '                prach_freq_offset = 2;\n'
        '                zero_correlation_zone_config = 5;\n'
        '            };\n'
        '        };\n'
        '        pdsch_cnfg =\n'
        '        {\n'
        '            p_b = 1;\n'
        '            rs_power = 0;\n'
        '        };\n'
        '        pusch_cnfg =\n'
        '        {\n'
        '            n_sb = 1;\n'
        '            hopping_mode = "inter-subframe";\n'
        '            pusch_hopping_offset = 2;\n'
        '            enable_64_qam = False;\n'
        '            ul_rs =\n'
        '            {\n'
        '                cyclic_shift = 0;\n'
        '                group_assignment_pusch = 0;\n'
        '                group_hopping_enabled = False;\n'
        '                sequence_hopping_enabled = False;\n'
        '            };\n'
        '        };\n'
        '        pucch_cnfg =\n'
        '        {\n'
        '            delta_pucch_shift = 2;\n'
        '            n_rb_cqi = 2;\n'
        '            n_cs_an = 0;\n'
        '            n1_pucch_an = 12;\n'
        '        };\n'
        '        ul_pwr_ctrl =\n'
        '        {\n'
        '            p0_nominal_pusch = -85;\n'
        '            alpha = 0.7;\n'
        '            p0_nominal_pucch = -107;\n'
        '            delta_flist_pucch =\n'
        '            {\n'
        '                format_1 = 0;\n'
        '                format_1b = 3;\n'
        '                format_2 = 1;\n'
        '                format_2a = 2;\n'
        '                format_2b = 2;\n'
        '            };\n'
        '            delta_preamble_msg3 = 6;\n'
        '        };\n'
        '        ul_cp_length = "len1";\n'
        '    };\n'
        '    ue_timers_and_constants =\n'
        '    {\n'
        '        t300 = 2000;\n'
        '        t301 = 100;\n'
        '        t310 = 200;\n'
        '        n310 = 1;\n'
        '        t311 = 10000;\n'
        '        n311 = 1;\n'
        '    };\n'
        '    freqInfo =\n'
        '    {\n'
        '        ul_carrier_freq_present = True;\n'
        '        ul_bw_present = True;\n'
        '        additional_spectrum_emission = 1;\n'
        '    };\n'
        '    time_alignment_timer = "INFINITY";\n'
        '};\n'
        'sib3 =\n'
        '{\n'
        '    cell_reselection_common =\n'
        '    {\n'
        '        q_hyst = 2;\n'
        '    };\n'
        '    cell_reselection_serving =\n'
        '    {\n'
        '        s_non_intra_search = 3;\n'
        '        thresh_serving_low = 2;\n'
        '        cell_resel_prio = 6;\n'
        '    };\n'
        '    intra_freq_reselection =\n'
        '    {\n'
        '        q_rx_lev_min = -61;\n'
        '        p_max = 23;\n'
        '        s_intra_search = 5;\n'
        '        presence_ant_port_1 = True;\n'
        '        neigh_cell_cnfg = 1;\n'
        '        t_resel_eutra = 1;\n'
        '    };\n'
        '};\n'
        'sib4 =\n'
        '{\n'
        '    intra_freq_neigh_cell_list =\n'
        '    (\n'
        '        {\n'
        '            phys_cell_id = 3;\n'
        '            q_offset_range = 24;\n'
        '        }\n'
        '    );\n'
        '};\n'
    )


def test_sib7():
    output = StringIO()
    SrsEnbSibs(
        SrsEnbSib1(intra_freq_reselection='Allowed', q_rx_lev_min=-65, cell_barred='NotBarred', si_window_length=20,
                   sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3, 7]),),
                   system_info_value_tag=0),
        SrsEnbSib2(
            rr_config_common_sib=SrsEnbSib2Rr(
                rach_cnfg=SrsEnbSib2RrRach(num_ra_preambles=52, preamble_init_rx_target_pwr=-104, pwr_ramping_step=6,
                                           preamble_trans_max=10, ra_resp_win_size=10, mac_con_res_timer=64,
                                           max_harq_msg3_tx=4),
                bcch_cnfg=SrsEnbSib2RrBcch(modification_period_coeff=16),
                pcch_cnfg=SrsEnbSib2RrPcch(default_paging_cycle=32, nB='1'),
                prach_cnfg=SrsEnbSib2RrPrach(
                    root_sequence_index=128,
                    prach_cnfg_info=SrsEnbSib2RrPrachInfo(high_speed_flag=False, prach_config_index=3,
                                                          prach_freq_offset=2,
                                                          zero_correlation_zone_config=5)
                ),
                pdsch_cnfg=SrsEnbSib2RrPdsch(p_b=1, rs_power=0),
                pusch_cnfg=SrsEnbSib2RrPusch(
                    n_sb=1, hopping_mode='inter-subframe', pusch_hopping_offset=2, enable_64_qam=False,
                    ul_rs=SrsEnbSib2RrPuschUlRs(cyclic_shift=0, group_assignment_pusch=0, group_hopping_enabled=False,
                                                sequence_hopping_enabled=False)
                ),
                pucch_cnfg=SrsEnbSib2RrPucch(delta_pucch_shift=2, n_rb_cqi=2, n_cs_an=0, n1_pucch_an=12),
                ul_pwr_ctrl=SrsEnbSib2RrUlPwrCtrl(
                    p0_nominal_pusch=-85, alpha=0.7, p0_nominal_pucch=-107, delta_preamble_msg3=6,
                    delta_flist_pucch=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch(
                        format_1=0, format_1b=3, format_2=1, format_2a=2, format_2b=2
                    )
                ),
                ul_cp_length='len1'
            ),
            ue_timers_and_constants=SrsEnbSib2UeTimersAndConstants(t300=2000, t301=100, t310=200, n310=1, t311=10000,
                                                                   n311=1),
            freqInfo=SrsEnbSib2FreqInfo(ul_carrier_freq_present=True, ul_bw_present=True,
                                        additional_spectrum_emission=1),
            time_alignment_timer='INFINITY'
        ),
        SrsEnbSib3(
            cell_reselection_common=SrsEnbSib3CellReselectionCommon(q_hyst=2),
            cell_reselection_serving=SrsEnbSib3CellReselectionServing(s_non_intra_search=3, thresh_serving_low=2,
                                                                      cell_resel_prio=6),
            intra_freq_reselection=SrsEnbSib3IntraFreqReselection(q_rx_lev_min=-61, p_max=23, s_intra_search=5,
                                                                  presence_ant_port_1=True, neigh_cell_cnfg=1,
                                                                  t_resel_eutra=1)
        ),
        sib7=SrsEnbSib7(
            t_resel_geran=1,
            carrier_freqs_info_list=(
                SrsEnbSib7CarrierFreqsInfo(cell_resel_prio=0, ncc_permitted=255, q_rx_lev_min=0, thresh_x_high=2,
                                           thresh_x_low=2, start_arfcn=871, band_ind='dcs1800',
                                           explicit_list_of_arfcns=(871,)),)
        )
    ).write(output)
    assert output.getvalue() == (
        'sib1 =\n'
        '{\n'
        '    intra_freq_reselection = "Allowed";\n'
        '    q_rx_lev_min = -65;\n'
        '    cell_barred = "NotBarred";\n'
        '    si_window_length = 20;\n'
        '    sched_info =\n'
        '    (\n'
        '        {\n'
        '            si_periodicity = 16;\n'
        '            si_mapping_info =\n'
        '            [\n'
        '                3,\n'
        '                7\n'
        '            ];\n'
        '        }\n'
        '    );\n'
        '    system_info_value_tag = 0;\n'
        '};\n'
        'sib2 =\n'
        '{\n'
        '    rr_config_common_sib =\n'
        '    {\n'
        '        rach_cnfg =\n'
        '        {\n'
        '            num_ra_preambles = 52;\n'
        '            preamble_init_rx_target_pwr = -104;\n'
        '            pwr_ramping_step = 6;\n'
        '            preamble_trans_max = 10;\n'
        '            ra_resp_win_size = 10;\n'
        '            mac_con_res_timer = 64;\n'
        '            max_harq_msg3_tx = 4;\n'
        '        };\n'
        '        bcch_cnfg =\n'
        '        {\n'
        '            modification_period_coeff = 16;\n'
        '        };\n'
        '        pcch_cnfg =\n'
        '        {\n'
        '            default_paging_cycle = 32;\n'
        '            nB = "1";\n'
        '        };\n'
        '        prach_cnfg =\n'
        '        {\n'
        '            root_sequence_index = 128;\n'
        '            prach_cnfg_info =\n'
        '            {\n'
        '                high_speed_flag = False;\n'
        '                prach_config_index = 3;\n'
        '                prach_freq_offset = 2;\n'
        '                zero_correlation_zone_config = 5;\n'
        '            };\n'
        '        };\n'
        '        pdsch_cnfg =\n'
        '        {\n'
        '            p_b = 1;\n'
        '            rs_power = 0;\n'
        '        };\n'
        '        pusch_cnfg =\n'
        '        {\n'
        '            n_sb = 1;\n'
        '            hopping_mode = "inter-subframe";\n'
        '            pusch_hopping_offset = 2;\n'
        '            enable_64_qam = False;\n'
        '            ul_rs =\n'
        '            {\n'
        '                cyclic_shift = 0;\n'
        '                group_assignment_pusch = 0;\n'
        '                group_hopping_enabled = False;\n'
        '                sequence_hopping_enabled = False;\n'
        '            };\n'
        '        };\n'
        '        pucch_cnfg =\n'
        '        {\n'
        '            delta_pucch_shift = 2;\n'
        '            n_rb_cqi = 2;\n'
        '            n_cs_an = 0;\n'
        '            n1_pucch_an = 12;\n'
        '        };\n'
        '        ul_pwr_ctrl =\n'
        '        {\n'
        '            p0_nominal_pusch = -85;\n'
        '            alpha = 0.7;\n'
        '            p0_nominal_pucch = -107;\n'
        '            delta_flist_pucch =\n'
        '            {\n'
        '                format_1 = 0;\n'
        '                format_1b = 3;\n'
        '                format_2 = 1;\n'
        '                format_2a = 2;\n'
        '                format_2b = 2;\n'
        '            };\n'
        '            delta_preamble_msg3 = 6;\n'
        '        };\n'
        '        ul_cp_length = "len1";\n'
        '    };\n'
        '    ue_timers_and_constants =\n'
        '    {\n'
        '        t300 = 2000;\n'
        '        t301 = 100;\n'
        '        t310 = 200;\n'
        '        n310 = 1;\n'
        '        t311 = 10000;\n'
        '        n311 = 1;\n'
        '    };\n'
        '    freqInfo =\n'
        '    {\n'
        '        ul_carrier_freq_present = True;\n'
        '        ul_bw_present = True;\n'
        '        additional_spectrum_emission = 1;\n'
        '    };\n'
        '    time_alignment_timer = "INFINITY";\n'
        '};\n'
        'sib3 =\n'
        '{\n'
        '    cell_reselection_common =\n'
        '    {\n'
        '        q_hyst = 2;\n'
        '    };\n'
        '    cell_reselection_serving =\n'
        '    {\n'
        '        s_non_intra_search = 3;\n'
        '        thresh_serving_low = 2;\n'
        '        cell_resel_prio = 6;\n'
        '    };\n'
        '    intra_freq_reselection =\n'
        '    {\n'
        '        q_rx_lev_min = -61;\n'
        '        p_max = 23;\n'
        '        s_intra_search = 5;\n'
        '        presence_ant_port_1 = True;\n'
        '        neigh_cell_cnfg = 1;\n'
        '        t_resel_eutra = 1;\n'
        '    };\n'
        '};\n'
        'sib7 =\n'
        '{\n'
        '    t_resel_geran = 1;\n'
        '    carrier_freqs_info_list =\n'
        '    (\n'
        '        {\n'
        '            cell_resel_prio = 0;\n'
        '            ncc_permitted = 255;\n'
        '            q_rx_lev_min = 0;\n'
        '            thresh_x_high = 2;\n'
        '            thresh_x_low = 2;\n'
        '            start_arfcn = 871;\n'
        '            band_ind = "dcs1800";\n'
        '            explicit_list_of_arfcns =\n'
        '            (\n'
        '                871\n'
        '            );\n'
        '        }\n'
        '    );\n'
        '};\n'
    )


def test_sib17():
    output = StringIO()
    SrsEnbSibs(
        SrsEnbSib1(intra_freq_reselection='Allowed', q_rx_lev_min=-65, cell_barred='NotBarred', si_window_length=20,
                   sched_info=(SrsEnbSib1SchedulerInfo(si_periodicity=16, si_mapping_info=[3, 7]),),
                   system_info_value_tag=0),
        SrsEnbSib2(
            rr_config_common_sib=SrsEnbSib2Rr(
                rach_cnfg=SrsEnbSib2RrRach(num_ra_preambles=52, preamble_init_rx_target_pwr=-104, pwr_ramping_step=6,
                                           preamble_trans_max=10, ra_resp_win_size=10, mac_con_res_timer=64,
                                           max_harq_msg3_tx=4),
                bcch_cnfg=SrsEnbSib2RrBcch(modification_period_coeff=16),
                pcch_cnfg=SrsEnbSib2RrPcch(default_paging_cycle=32, nB='1'),
                prach_cnfg=SrsEnbSib2RrPrach(
                    root_sequence_index=128,
                    prach_cnfg_info=SrsEnbSib2RrPrachInfo(high_speed_flag=False, prach_config_index=3,
                                                          prach_freq_offset=2,
                                                          zero_correlation_zone_config=5)
                ),
                pdsch_cnfg=SrsEnbSib2RrPdsch(p_b=1, rs_power=0),
                pusch_cnfg=SrsEnbSib2RrPusch(
                    n_sb=1, hopping_mode='inter-subframe', pusch_hopping_offset=2, enable_64_qam=False,
                    ul_rs=SrsEnbSib2RrPuschUlRs(cyclic_shift=0, group_assignment_pusch=0, group_hopping_enabled=False,
                                                sequence_hopping_enabled=False)
                ),
                pucch_cnfg=SrsEnbSib2RrPucch(delta_pucch_shift=2, n_rb_cqi=2, n_cs_an=0, n1_pucch_an=12),
                ul_pwr_ctrl=SrsEnbSib2RrUlPwrCtrl(
                    p0_nominal_pusch=-85, alpha=0.7, p0_nominal_pucch=-107, delta_preamble_msg3=6,
                    delta_flist_pucch=SrsEnbSib2RrUlPwrCtrlDeltaFlistPucch(
                        format_1=0, format_1b=3, format_2=1, format_2a=2, format_2b=2
                    )
                ),
                ul_cp_length='len1'
            ),
            ue_timers_and_constants=SrsEnbSib2UeTimersAndConstants(t300=2000, t301=100, t310=200, n310=1, t311=10000,
                                                                   n311=1),
            freqInfo=SrsEnbSib2FreqInfo(ul_carrier_freq_present=True, ul_bw_present=True,
                                        additional_spectrum_emission=1),
            time_alignment_timer='INFINITY'
        ),
        SrsEnbSib3(
            cell_reselection_common=SrsEnbSib3CellReselectionCommon(q_hyst=2),
            cell_reselection_serving=SrsEnbSib3CellReselectionServing(s_non_intra_search=3, thresh_serving_low=2,
                                                                      cell_resel_prio=6),
            intra_freq_reselection=SrsEnbSib3IntraFreqReselection(q_rx_lev_min=-61, p_max=23, s_intra_search=5,
                                                                  presence_ant_port_1=True, neigh_cell_cnfg=1,
                                                                  t_resel_eutra=1)
        ),
        sib17=SrsEnbSib17((
            SrsEnbSib17InfoPerPlmn(wlan_id_list=(
                SrsEnbSib17WlanId(ssid='hey'), SrsEnbSib17WlanId(ssid='hey1', bssid='313233343536'),
                SrsEnbSib17WlanId(bssid='313233343537')
            )),
        ))
    ).write(output)
    assert output.getvalue() == (
        'sib1 =\n'
        '{\n'
        '    intra_freq_reselection = "Allowed";\n'
        '    q_rx_lev_min = -65;\n'
        '    cell_barred = "NotBarred";\n'
        '    si_window_length = 20;\n'
        '    sched_info =\n'
        '    (\n'
        '        {\n'
        '            si_periodicity = 16;\n'
        '            si_mapping_info =\n'
        '            [\n'
        '                3,\n'
        '                7\n'
        '            ];\n'
        '        }\n'
        '    );\n'
        '    system_info_value_tag = 0;\n'
        '};\n'
        'sib2 =\n'
        '{\n'
        '    rr_config_common_sib =\n'
        '    {\n'
        '        rach_cnfg =\n'
        '        {\n'
        '            num_ra_preambles = 52;\n'
        '            preamble_init_rx_target_pwr = -104;\n'
        '            pwr_ramping_step = 6;\n'
        '            preamble_trans_max = 10;\n'
        '            ra_resp_win_size = 10;\n'
        '            mac_con_res_timer = 64;\n'
        '            max_harq_msg3_tx = 4;\n'
        '        };\n'
        '        bcch_cnfg =\n'
        '        {\n'
        '            modification_period_coeff = 16;\n'
        '        };\n'
        '        pcch_cnfg =\n'
        '        {\n'
        '            default_paging_cycle = 32;\n'
        '            nB = "1";\n'
        '        };\n'
        '        prach_cnfg =\n'
        '        {\n'
        '            root_sequence_index = 128;\n'
        '            prach_cnfg_info =\n'
        '            {\n'
        '                high_speed_flag = False;\n'
        '                prach_config_index = 3;\n'
        '                prach_freq_offset = 2;\n'
        '                zero_correlation_zone_config = 5;\n'
        '            };\n'
        '        };\n'
        '        pdsch_cnfg =\n'
        '        {\n'
        '            p_b = 1;\n'
        '            rs_power = 0;\n'
        '        };\n'
        '        pusch_cnfg =\n'
        '        {\n'
        '            n_sb = 1;\n'
        '            hopping_mode = "inter-subframe";\n'
        '            pusch_hopping_offset = 2;\n'
        '            enable_64_qam = False;\n'
        '            ul_rs =\n'
        '            {\n'
        '                cyclic_shift = 0;\n'
        '                group_assignment_pusch = 0;\n'
        '                group_hopping_enabled = False;\n'
        '                sequence_hopping_enabled = False;\n'
        '            };\n'
        '        };\n'
        '        pucch_cnfg =\n'
        '        {\n'
        '            delta_pucch_shift = 2;\n'
        '            n_rb_cqi = 2;\n'
        '            n_cs_an = 0;\n'
        '            n1_pucch_an = 12;\n'
        '        };\n'
        '        ul_pwr_ctrl =\n'
        '        {\n'
        '            p0_nominal_pusch = -85;\n'
        '            alpha = 0.7;\n'
        '            p0_nominal_pucch = -107;\n'
        '            delta_flist_pucch =\n'
        '            {\n'
        '                format_1 = 0;\n'
        '                format_1b = 3;\n'
        '                format_2 = 1;\n'
        '                format_2a = 2;\n'
        '                format_2b = 2;\n'
        '            };\n'
        '            delta_preamble_msg3 = 6;\n'
        '        };\n'
        '        ul_cp_length = "len1";\n'
        '    };\n'
        '    ue_timers_and_constants =\n'
        '    {\n'
        '        t300 = 2000;\n'
        '        t301 = 100;\n'
        '        t310 = 200;\n'
        '        n310 = 1;\n'
        '        t311 = 10000;\n'
        '        n311 = 1;\n'
        '    };\n'
        '    freqInfo =\n'
        '    {\n'
        '        ul_carrier_freq_present = True;\n'
        '        ul_bw_present = True;\n'
        '        additional_spectrum_emission = 1;\n'
        '    };\n'
        '    time_alignment_timer = "INFINITY";\n'
        '};\n'
        'sib3 =\n'
        '{\n'
        '    cell_reselection_common =\n'
        '    {\n'
        '        q_hyst = 2;\n'
        '    };\n'
        '    cell_reselection_serving =\n'
        '    {\n'
        '        s_non_intra_search = 3;\n'
        '        thresh_serving_low = 2;\n'
        '        cell_resel_prio = 6;\n'
        '    };\n'
        '    intra_freq_reselection =\n'
        '    {\n'
        '        q_rx_lev_min = -61;\n'
        '        p_max = 23;\n'
        '        s_intra_search = 5;\n'
        '        presence_ant_port_1 = True;\n'
        '        neigh_cell_cnfg = 1;\n'
        '        t_resel_eutra = 1;\n'
        '    };\n'
        '};\n'
        'sib17 =\n'
        '{\n'
        '    wlan_offload_info_per_plmn_list =\n'
        '    (\n'
        '        {\n'
        '            wlan_offload_cfg_common =\n'
        '            {\n'
        '                thres_rsrp =\n'
        '                {\n'
        '                    thres_rsrp_low = 97;\n'
        '                    thres_rsrp_high = 97;\n'
        '                };\n'
        '                thres_rsrq =\n'
        '                {\n'
        '                    thres_rsrq_low = 34;\n'
        '                    thres_rsrq_high = 34;\n'
        '                };\n'
        '                thres_ch_utilization =\n'
        '                {\n'
        '                    thres_ch_utilization_low = 255;\n'
        '                    thres_ch_utilization_high = 255;\n'
        '                };\n'
        '                thres_backhaul_bw =\n'
        '                {\n'
        '                    thres_backhaul_dl_bw_low = 0;\n'
        '                    thres_backhaul_dl_bw_high = 0;\n'
        '                    thres_backhaul_ul_bw_low = 0;\n'
        '                    thres_backhaul_ul_bw_high = 0;\n'
        '                };\n'
        '                thres_wlan_rssi =\n'
        '                {\n'
        '                    thres_wlan_rssi_low = 0;\n'
        '                    thres_wlan_rssi_high = 0;\n'
        '                };\n'
        '                t_steering_wlan = 1;\n'
        '            };\n'
        '            wlan_id_list =\n'
        '            (\n'
        '                {\n'
        '                    ssid = "hey";\n'
        '                },\n'
        '                {\n'
        '                    ssid = "hey1";\n'
        '                    bssid = "313233343536";\n'
        '                },\n'
        '                {\n'
        '                    bssid = "313233343537";\n'
        '                }\n'
        '            );\n'
        '        }\n'
        '    );\n'
        '};\n'
    )
