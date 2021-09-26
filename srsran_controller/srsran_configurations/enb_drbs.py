from dataclasses import dataclass, asdict
from typing import TextIO

import libconf

from srsran_controller.common.dataclasses import to_dict_without_none

__all__ = [
    'SrsEnbDrbQciConfigPdcpConfig', 'SrsEnbDrbQciConfigRlcConfigUlUm', 'SrsEnbDrbQciConfigRlcConfigDlUm',
    'SrsEnbDrbQciConfigRlcConfigUlAm', 'SrsEnbDrbQciConfigRlcConfigDlAm', 'SrsEnbDrbQciConfigRlcConfig',
    'SrsEnbDrbQciConfigLogicalChannelConfig', 'SrsEnbDrbQciConfig', 'SrsEnbDrbs'
]


@dataclass
class SrsEnbDrbQciConfigPdcpConfig:
    discard_timer: int = None
    pdcp_sn_size: int = None
    status_report_required: bool = None


@dataclass
class SrsEnbDrbQciConfigRlcConfigUlUm:
    sn_field_length: int


@dataclass
class SrsEnbDrbQciConfigRlcConfigDlUm:
    sn_field_length: int
    t_reordering: int


@dataclass
class SrsEnbDrbQciConfigRlcConfigUlAm:
    t_poll_retx: int
    poll_pdu: int
    poll_byte: int
    max_retx_thresh: int


@dataclass
class SrsEnbDrbQciConfigRlcConfigDlAm:
    t_reordering: int
    t_status_prohibit: int


@dataclass
class SrsEnbDrbQciConfigRlcConfig:
    ul_um: SrsEnbDrbQciConfigRlcConfigUlUm = None
    dl_um: SrsEnbDrbQciConfigRlcConfigDlUm = None
    ul_am: SrsEnbDrbQciConfigRlcConfigUlAm = None
    dl_am: SrsEnbDrbQciConfigRlcConfigDlAm = None


@dataclass
class SrsEnbDrbQciConfigLogicalChannelConfig:
    priority: int
    prioritized_bit_rate: int
    bucket_size_duration: int
    log_chan_group: int


@dataclass
class SrsEnbDrbQciConfig:
    qci: int
    pdcp_config: SrsEnbDrbQciConfigPdcpConfig
    rlc_config: SrsEnbDrbQciConfigRlcConfig
    logical_channel_config: SrsEnbDrbQciConfigLogicalChannelConfig

    def to_dict(self):
        original_dict = asdict(self)
        original_dict['pdcp_config'] = to_dict_without_none(self.pdcp_config)
        original_dict['rlc_config'] = to_dict_without_none(self.rlc_config)
        return original_dict


@dataclass
class SrsEnbDrbs:
    qci_config: tuple[SrsEnbDrbQciConfig, ...]

    def write(self, fd: TextIO):
        libconf.dump({'qci_config': tuple(config.to_dict() for config in self.qci_config)}, fd)
