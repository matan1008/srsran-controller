from srsran_controller.srsran_configurations.enb_rbs import *
from io import StringIO


def test_sanity():
    output = StringIO()
    SrsEnbRbs(qci_config=(
        SrsEnbRbQciConfig(
            qci=7,
            pdcp_config=SrsEnbRbQciConfigPdcpConfig(discard_timer=100, pdcp_sn_size=12),
            rlc_config=SrsEnbRbQciConfigRlcConfig(
                ul_um=SrsEnbRbQciConfigRlcConfigUlUm(sn_field_length=10),
                dl_um=SrsEnbRbQciConfigRlcConfigDlUm(sn_field_length=10, t_reordering=45)
            ),
            logical_channel_config=SrsEnbRbQciConfigLogicalChannelConfig(
                priority=13, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=2
            )
        ),
        SrsEnbRbQciConfig(
            qci=9,
            pdcp_config=SrsEnbRbQciConfigPdcpConfig(discard_timer=-1, status_report_required=True),
            rlc_config=SrsEnbRbQciConfigRlcConfig(
                ul_am=SrsEnbRbQciConfigRlcConfigUlAm(t_poll_retx=120, poll_pdu=64, poll_byte=750, max_retx_thresh=16),
                dl_am=SrsEnbRbQciConfigRlcConfigDlAm(t_reordering=50, t_status_prohibit=50)
            ),
            logical_channel_config=SrsEnbRbQciConfigLogicalChannelConfig(
                priority=11, prioritized_bit_rate=-1, bucket_size_duration=100, log_chan_group=3
            )
        ),
    )).write(output)
    assert output.getvalue() == (
        'qci_config =\n'
        '(\n'
        '    {\n'
        '        qci = 7;\n'
        '        pdcp_config =\n'
        '        {\n'
        '            discard_timer = 100;\n'
        '            pdcp_sn_size = 12;\n'
        '        };\n'
        '        rlc_config =\n'
        '        {\n'
        '            ul_um =\n'
        '            {\n'
        '                sn_field_length = 10;\n'
        '            };\n'
        '            dl_um =\n'
        '            {\n'
        '                sn_field_length = 10;\n'
        '                t_reordering = 45;\n'
        '            };\n'
        '        };\n'
        '        logical_channel_config =\n'
        '        {\n'
        '            priority = 13;\n'
        '            prioritized_bit_rate = -1;\n'
        '            bucket_size_duration = 100;\n'
        '            log_chan_group = 2;\n'
        '        };\n'
        '    },\n'
        '    {\n'
        '        qci = 9;\n'
        '        pdcp_config =\n'
        '        {\n'
        '            discard_timer = -1;\n'
        '            status_report_required = True;\n'
        '        };\n'
        '        rlc_config =\n'
        '        {\n'
        '            ul_am =\n'
        '            {\n'
        '                t_poll_retx = 120;\n'
        '                poll_pdu = 64;\n'
        '                poll_byte = 750;\n'
        '                max_retx_thresh = 16;\n'
        '            };\n'
        '            dl_am =\n'
        '            {\n'
        '                t_reordering = 50;\n'
        '                t_status_prohibit = 50;\n'
        '            };\n'
        '        };\n'
        '        logical_channel_config =\n'
        '        {\n'
        '            priority = 11;\n'
        '            prioritized_bit_rate = -1;\n'
        '            bucket_size_duration = 100;\n'
        '            log_chan_group = 3;\n'
        '        };\n'
        '    }\n'
        ');\n'
    )
