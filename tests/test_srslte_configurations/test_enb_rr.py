from io import StringIO

from srslte_controller.srslte_configurations.enb_rr import *


def test_sanity():
    output = StringIO()
    SrsEnbRR(
        mac_cnfg=SrsEnbRRMacConfig(
            phr_cnfg=SrsEnbRRMacConfigPhr(dl_pathloss_change='dB3', periodic_phr_timer=50, prohibit_phr_timer=0),
            ulsch_cnfg=SrsEnbRRMacConfigUlsch(max_harq_tx=4, periodic_bsr_timer=20, retx_bsr_timer=320),
            time_alignment_timer=-1
        ),
        phy_cnfg=SrsEnbRRPhyConfig(
            phich_cnfg=SrsEnbRRPhyConfigPhich(duration='Normal', resources='1/6'),
            pusch_cnfg_ded=SrsEnbRRPhyConfigPuschDed(beta_offset_ack_idx=6, beta_offset_ri_idx=6,
                                                     beta_offset_cqi_idx=6),
            sched_request_cnfg=SrsEnbRRPhyConfigSchedRequest(dsr_trans_max=64, period=20, nof_prb=2),
            cqi_report_cnfg=SrsEnbRRPhyConfigCqiReport(
                mode='periodic', simultaneousAckCQI=True, period=40, nof_prb=2, m_ri=8
            )
        ),
        cell_list=(SrsEnbRRCell(
            cell_id=0x01, tac=0x0007, pci=1, dl_earfcn=3350, ho_active=False, scell_list=(),
            meas_cell_list=(SrsEnbRRCellListMeasCell(eci=0x19C02, dl_earfcn=2850, pci=2),),
            meas_report_desc=SrsEnbRRCellListMeasReportDesc(
                a3_report_type='RSRP', a3_offset=6, a3_hysteresis=0, a3_time_to_trigger=480, rsrq_config=4
            )
        ),)
    ).write(output)
    assert output.getvalue() == (
        'mac_cnfg =\n'
        '{\n'
        '    phr_cnfg =\n'
        '    {\n'
        '        dl_pathloss_change = "dB3";\n'
        '        periodic_phr_timer = 50;\n'
        '        prohibit_phr_timer = 0;\n'
        '    };\n'
        '    ulsch_cnfg =\n'
        '    {\n'
        '        max_harq_tx = 4;\n'
        '        periodic_bsr_timer = 20;\n'
        '        retx_bsr_timer = 320;\n'
        '    };\n'
        '    time_alignment_timer = -1;\n'
        '};\n'
        'phy_cnfg =\n'
        '{\n'
        '    phich_cnfg =\n'
        '    {\n'
        '        duration = "Normal";\n'
        '        resources = "1/6";\n'
        '    };\n'
        '    pusch_cnfg_ded =\n'
        '    {\n'
        '        beta_offset_ack_idx = 6;\n'
        '        beta_offset_ri_idx = 6;\n'
        '        beta_offset_cqi_idx = 6;\n'
        '    };\n'
        '    sched_request_cnfg =\n'
        '    {\n'
        '        dsr_trans_max = 64;\n'
        '        period = 20;\n'
        '        nof_prb = 2;\n'
        '    };\n'
        '    cqi_report_cnfg =\n'
        '    {\n'
        '        mode = "periodic";\n'
        '        simultaneousAckCQI = True;\n'
        '        period = 40;\n'
        '        nof_prb = 2;\n'
        '        m_ri = 8;\n'
        '    };\n'
        '};\n'
        'cell_list =\n'
        '(\n'
        '    {\n'
        '        cell_id = 1;\n'
        '        tac = 7;\n'
        '        pci = 1;\n'
        '        dl_earfcn = 3350;\n'
        '        rf_port = 0;\n'
        '        ho_active = False;\n'
        '        scell_list =\n'
        '        (\n'
        '\n'
        '        );\n'
        '        meas_cell_list =\n'
        '        (\n'
        '            {\n'
        '                eci = 105474;\n'
        '                dl_earfcn = 2850;\n'
        '                pci = 2;\n'
        '            }\n'
        '        );\n'
        '        meas_report_desc =\n'
        '        {\n'
        '            a3_report_type = "RSRP";\n'
        '            a3_offset = 6;\n'
        '            a3_hysteresis = 0;\n'
        '            a3_time_to_trigger = 480;\n'
        '            rsrq_config = 4;\n'
        '        };\n'
        '    }\n'
        ');\n'
    )


def test_multi_cell():
    output = StringIO()
    SrsEnbRR(
        mac_cnfg=SrsEnbRRMacConfig(
            phr_cnfg=SrsEnbRRMacConfigPhr(dl_pathloss_change='dB3', periodic_phr_timer=50, prohibit_phr_timer=0),
            ulsch_cnfg=SrsEnbRRMacConfigUlsch(max_harq_tx=4, periodic_bsr_timer=20, retx_bsr_timer=320),
            time_alignment_timer=-1
        ),
        phy_cnfg=SrsEnbRRPhyConfig(
            phich_cnfg=SrsEnbRRPhyConfigPhich(duration='Normal', resources='1/6'),
            pusch_cnfg_ded=SrsEnbRRPhyConfigPuschDed(beta_offset_ack_idx=6, beta_offset_ri_idx=6,
                                                     beta_offset_cqi_idx=6),
            sched_request_cnfg=SrsEnbRRPhyConfigSchedRequest(dsr_trans_max=64, period=20, nof_prb=2),
            cqi_report_cnfg=SrsEnbRRPhyConfigCqiReport(
                mode='periodic', simultaneousAckCQI=True, period=40, nof_prb=2, m_ri=8
            )
        ),
        cell_list=(
            SrsEnbRRCell(
                cell_id=0x01, tac=0x0007, pci=1, dl_earfcn=3350, ho_active=False, scell_list=(),
                meas_cell_list=(SrsEnbRRCellListMeasCell(eci=0x19C02, dl_earfcn=2850, pci=2),),
                meas_report_desc=SrsEnbRRCellListMeasReportDesc(
                    a3_report_type='RSRP', a3_offset=6, a3_hysteresis=0, a3_time_to_trigger=480, rsrq_config=4
                )
            ),
            SrsEnbRRCell(
                cell_id=0x02, tac=0x0007, pci=2, dl_earfcn=1600, ho_active=False, scell_list=(), rf_port=1,
                meas_cell_list=(SrsEnbRRCellListMeasCell(eci=0x19C01, dl_earfcn=3350, pci=1),)
            ),
        )
    ).write(output)
    assert output.getvalue() == (
        'mac_cnfg =\n'
        '{\n'
        '    phr_cnfg =\n'
        '    {\n'
        '        dl_pathloss_change = "dB3";\n'
        '        periodic_phr_timer = 50;\n'
        '        prohibit_phr_timer = 0;\n'
        '    };\n'
        '    ulsch_cnfg =\n'
        '    {\n'
        '        max_harq_tx = 4;\n'
        '        periodic_bsr_timer = 20;\n'
        '        retx_bsr_timer = 320;\n'
        '    };\n'
        '    time_alignment_timer = -1;\n'
        '};\n'
        'phy_cnfg =\n'
        '{\n'
        '    phich_cnfg =\n'
        '    {\n'
        '        duration = "Normal";\n'
        '        resources = "1/6";\n'
        '    };\n'
        '    pusch_cnfg_ded =\n'
        '    {\n'
        '        beta_offset_ack_idx = 6;\n'
        '        beta_offset_ri_idx = 6;\n'
        '        beta_offset_cqi_idx = 6;\n'
        '    };\n'
        '    sched_request_cnfg =\n'
        '    {\n'
        '        dsr_trans_max = 64;\n'
        '        period = 20;\n'
        '        nof_prb = 2;\n'
        '    };\n'
        '    cqi_report_cnfg =\n'
        '    {\n'
        '        mode = "periodic";\n'
        '        simultaneousAckCQI = True;\n'
        '        period = 40;\n'
        '        nof_prb = 2;\n'
        '        m_ri = 8;\n'
        '    };\n'
        '};\n'
        'cell_list =\n'
        '(\n'
        '    {\n'
        '        cell_id = 1;\n'
        '        tac = 7;\n'
        '        pci = 1;\n'
        '        dl_earfcn = 3350;\n'
        '        rf_port = 0;\n'
        '        ho_active = False;\n'
        '        scell_list =\n'
        '        (\n'
        '\n'
        '        );\n'
        '        meas_cell_list =\n'
        '        (\n'
        '            {\n'
        '                eci = 105474;\n'
        '                dl_earfcn = 2850;\n'
        '                pci = 2;\n'
        '            }\n'
        '        );\n'
        '        meas_report_desc =\n'
        '        {\n'
        '            a3_report_type = "RSRP";\n'
        '            a3_offset = 6;\n'
        '            a3_hysteresis = 0;\n'
        '            a3_time_to_trigger = 480;\n'
        '            rsrq_config = 4;\n'
        '        };\n'
        '    },\n'
        '    {\n'
        '        cell_id = 2;\n'
        '        tac = 7;\n'
        '        pci = 2;\n'
        '        dl_earfcn = 1600;\n'
        '        rf_port = 1;\n'
        '        ho_active = False;\n'
        '        scell_list =\n'
        '        (\n'
        '\n'
        '        );\n'
        '        meas_cell_list =\n'
        '        (\n'
        '            {\n'
        '                eci = 105473;\n'
        '                dl_earfcn = 3350;\n'
        '                pci = 1;\n'
        '            }\n'
        '        );\n'
        '        meas_report_desc =\n'
        '        {\n'
        '            a3_report_type = "RSRP";\n'
        '            a3_offset = 6;\n'
        '            a3_hysteresis = 0;\n'
        '            a3_time_to_trigger = 480;\n'
        '            rsrq_config = 4;\n'
        '        };\n'
        '    }\n'
        ');\n'
    )
