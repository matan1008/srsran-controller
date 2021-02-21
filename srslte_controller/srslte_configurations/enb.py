import configparser
from dataclasses import dataclass, asdict, field
from typing import TextIO


@dataclass
class SrsEnbEnbConfiguration:
    enb_id: int
    mcc: str
    mnc: str
    mme_addr: str
    gtp_bind_addr: str
    s1c_bind_addr: str
    n_prb: int = 50


@dataclass
class SrsEnbEnbFilesConfiguration:
    sib_config: str
    rr_config: str
    drb_config: str


@dataclass
class SrsEnbRfConfiguration:
    device_name: str = 'auto'
    device_args: str = 'auto'
    time_adv_nsamples: str = 'auto'
    tx_gain: int = 80
    rx_gain: int = 40


@dataclass
class SrsEnbPcapConfiguration:
    filename: str
    s1ap_filename: str
    enable: bool = True
    s1ap_enable: bool = True


@dataclass
class SrsEnbLogConfiguration:
    rf_level: str = 'info'
    phy_level: str = 'info'
    phy_lib_level: str = 'info'
    mac_level: str = 'info'
    rlc_level: str = 'info'
    pdcp_level: str = 'info'
    rrc_level: str = 'info'
    gtpu_level: str = 'info'
    s1ap_level: str = 'info'
    stack_level: str = 'info'
    filename: str = '/tmp/enb.log'
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
                    'gtpu_level', 's1ap_level', 'stack_level'
            ):
                del log[entry]
        return log


@dataclass
class SrsEnbConfiguration:
    enb: SrsEnbEnbConfiguration
    enb_files: SrsEnbEnbFilesConfiguration
    rf: SrsEnbRfConfiguration
    pcap: SrsEnbPcapConfiguration = field(default_factory=lambda: SrsEnbPcapConfiguration(
        enable=False, filename='/tmp/epc.pcap', s1ap_enable=False, s1ap_filename='/tmp/s1ap_epc.pcap'
    ))
    log: SrsEnbLogConfiguration = field(default_factory=lambda: SrsEnbLogConfiguration())

    def write(self, fd: TextIO):
        config = configparser.ConfigParser()
        config['enb'] = asdict(self.enb)
        config['enb_files'] = asdict(self.enb_files)
        config['rf'] = asdict(self.rf)
        config['pcap'] = asdict(self.pcap)
        config['log'] = self.log.to_dict()
        config.write(fd)
