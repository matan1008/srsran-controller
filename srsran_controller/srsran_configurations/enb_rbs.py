from dataclasses import dataclass, asdict
from typing import TextIO

import libconf

from srsran_controller.common.dataclasses import to_dict_without_none

__all__ = [
    'SrsEnbRbQciConfigPdcpConfig', 'SrsEnbRbQciConfigRlcConfigUlUm', 'SrsEnbRbQciConfigRlcConfigDlUm',
    'SrsEnbRbQciConfigRlcConfigUlAm', 'SrsEnbRbQciConfigRlcConfigDlAm', 'SrsEnbRbQciConfigRlcConfig',
    'SrsEnbRbQciConfigLogicalChannelConfig', 'SrsEnbRbQciConfig', 'SrsEnbRbs'
]


@dataclass
class SrsEnbRbQciConfigPdcpConfig:
    discard_timer: int = None
    pdcp_sn_size: int = None
    status_report_required: bool = None


@dataclass
class SrsEnbRbQciConfigRlcConfigUlUm:
    sn_field_length: int


@dataclass
class SrsEnbRbQciConfigRlcConfigDlUm:
    sn_field_length: int
    t_reordering: int


@dataclass
class SrsEnbRbQciConfigRlcConfigUlAm:
    t_poll_retx: int
    poll_pdu: int
    poll_byte: int
    max_retx_thresh: int


@dataclass
class SrsEnbRbQciConfigRlcConfigDlAm:
    t_reordering: int
    t_status_prohibit: int


@dataclass
class SrsEnbRbQciConfigRlcConfig:
    ul_um: SrsEnbRbQciConfigRlcConfigUlUm = None
    dl_um: SrsEnbRbQciConfigRlcConfigDlUm = None
    ul_am: SrsEnbRbQciConfigRlcConfigUlAm = None
    dl_am: SrsEnbRbQciConfigRlcConfigDlAm = None


@dataclass
class SrsEnbRbQciConfigLogicalChannelConfig:
    priority: int
    prioritized_bit_rate: int
    bucket_size_duration: int
    log_chan_group: int


@dataclass
class SrsEnbRbQciConfig:
    qci: int
    pdcp_config: SrsEnbRbQciConfigPdcpConfig
    rlc_config: SrsEnbRbQciConfigRlcConfig
    logical_channel_config: SrsEnbRbQciConfigLogicalChannelConfig

    def to_dict(self):
        original_dict = asdict(self)
        original_dict['pdcp_config'] = to_dict_without_none(self.pdcp_config)
        original_dict['rlc_config'] = to_dict_without_none(self.rlc_config)
        return original_dict


@dataclass
class SrsEnbRbs:
    qci_config: tuple[SrsEnbRbQciConfig, ...]

    def write(self, fd: TextIO):
        libconf.dump({'qci_config': tuple(config.to_dict() for config in self.qci_config)}, fd)
