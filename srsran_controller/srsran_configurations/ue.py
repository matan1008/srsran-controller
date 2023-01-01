import configparser
from dataclasses import dataclass, asdict, field
from io import StringIO
from typing import TextIO

from srsran_controller.common.dataclasses import to_dict_without_none

__all__ = [
    'SrsUeRfConfiguration', 'SrsUeRatEutraConfiguration', 'SrsUePcapConfiguration', 'SrsUeLogConfiguration',
    'SrsUeUsimConfiguration', 'SrsUePhyConfiguration', 'SrsUeConfiguration'
]


@dataclass
class SrsUeRfConfiguration:
    device_name: str = 'auto'
    device_args: str = 'auto'
    time_adv_nsamples: str = None
    tx_gain: int = 80
    rx_gain: int = 70


@dataclass
class SrsUeRatEutraConfiguration:
    dl_earfcn: int


@dataclass
class SrsUePcapConfiguration:
    enable: str = 'none'
    mac_filename: str = '/tmp/ue_mac.pcap'
    mac_net_enable: bool = False
    bind_ip: str = '0.0.0.0'
    bind_port: int = 5687
    client_ip: str = '127.0.0.1'
    client_port: int = 5847


@dataclass
class SrsUeLogConfiguration:
    rf_level: str = 'info'
    phy_level: str = 'info'
    phy_lib_level: str = 'info'
    mac_level: str = 'info'
    rlc_level: str = 'info'
    pdcp_level: str = 'info'
    rrc_level: str = 'debug'
    nas_level: str = 'info'
    gw_level: str = 'info'
    usim_level: str = 'info'
    stack_level: str = 'info'
    filename: str = '/tmp/ue.log'
    all_hex_limit: int = 64
    all_level: str = ''
    file_max_size: int = -1

    def to_dict(self):
        log = asdict(self)
        if not self.all_level:
            del log['all_level']
        else:
            for entry in (
                    'rf_level', 'phy_level', 'phy_lib_level', 'mac_level', 'rlc_level', 'pdcp_level', 'rrc_level',
                    'nas_level', 'gw_level', 'usim_level', 'stack_level'
            ):
                del log[entry]
        return log


@dataclass
class SrsUeUsimConfiguration:
    opc: str
    k: str
    imsi: str
    imei: str
    algo: str = 'mil'
    mode: str = 'soft'


@dataclass
class SrsUePhyConfiguration:
    in_sync_rsrp_dbm_th: float = -160.0
    in_sync_snr_db_th: float = -10.0
    nof_out_of_sync_events: int = 40
    force_N_id_2: int = -1
    force_N_id_1: int = -1


@dataclass
class SrsUeConfiguration:
    rat_eutra: SrsUeRatEutraConfiguration
    pcap: SrsUePcapConfiguration
    usim: SrsUeUsimConfiguration
    rf: SrsUeRfConfiguration = field(default_factory=lambda: SrsUeRfConfiguration())
    log: SrsUeLogConfiguration = field(default_factory=lambda: SrsUeLogConfiguration())
    phy: SrsUePhyConfiguration = field(default_factory=lambda: SrsUePhyConfiguration())

    def write(self, fd: TextIO):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['rat.eutra'] = asdict(self.rat_eutra)
        config['pcap'] = asdict(self.pcap)
        config['usim'] = asdict(self.usim)
        config['rf'] = to_dict_without_none(self.rf)
        config['log'] = self.log.to_dict()
        config['phy'] = asdict(self.phy)
        config.write(fd)

    def __str__(self):
        data = StringIO()
        self.write(data)
        return data.getvalue()
