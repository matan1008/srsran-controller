import configparser
from dataclasses import dataclass, field, asdict
from typing import TextIO

__all__ = [
    'SrsEpcMmeConfiguration', 'SrsEpcHssConfiguration', 'SrsEpcSpgwConfiguration', 'SrsEpcPcapConfiguration',
    'SrsEpcLogConfiguration', 'SrsEpcConfiguration'
]


@dataclass
class SrsEpcMmeConfiguration:
    mme_code: str
    mme_group: str
    tac: int
    mcc: str
    mnc: str
    mme_bind_addr: str
    apn: str
    full_net_name: str
    short_net_name: str
    dns_addr: str = '8.8.8.8'
    encryption_algo: str = 'EEA0'
    integrity_algo: str = 'EIA1'
    paging_timer: int = 2
    request_imeisv: bool = True

    def to_dict(self):
        mme = asdict(self)
        mme['tac'] = hex(mme['tac'])
        return mme


@dataclass
class SrsEpcHssConfiguration:
    db_file: str


@dataclass
class SrsEpcSpgwConfiguration:
    gtpu_bind_addr: str
    sgi_if_addr: str = '172.16.0.1'
    sgi_if_name: str = 'srs_spgw_sgi'
    max_paging_queue: int = 100


@dataclass
class SrsEpcPcapConfiguration:
    filename: str
    enable: bool = True


@dataclass
class SrsEpcLogConfiguration:
    nas_level: str = 'info'
    s1ap_level: str = 'info'
    mme_gtpc_level: str = 'info'
    spgw_gtpc_level: str = 'info'
    gtpu_level: str = 'info'
    spgw_level: str = 'info'
    hss_level: str = 'info'
    filename: str = '/tmp/epc.log'
    all_hex_limit: int = 64
    all_level: str = ''

    def to_dict(self):
        log = asdict(self)
        if not self.all_level:
            del log['all_level']
        else:
            for entry in (
                    'nas_level', 's1ap_level', 'mme_gtpc_level', 'spgw_gtpc_level', 'gtpu_level', 'spgw_level',
                    'hss_level',
            ):
                del log[entry]
        return log


@dataclass
class SrsEpcConfiguration:
    mme: SrsEpcMmeConfiguration
    hss: SrsEpcHssConfiguration
    spgw: SrsEpcSpgwConfiguration
    pcap: SrsEpcPcapConfiguration = field(
        default_factory=lambda: SrsEpcPcapConfiguration(enable=False, filename='/tmp/epc.pcap')
    )
    log: SrsEpcLogConfiguration = field(default_factory=lambda: SrsEpcLogConfiguration())

    def write(self, fd: TextIO):
        config = configparser.ConfigParser()
        config['mme'] = self.mme.to_dict()
        config['hss'] = asdict(self.hss)
        config['spgw'] = asdict(self.spgw)
        config['pcap'] = asdict(self.pcap)
        config['log'] = self.log.to_dict()
        config.write(fd)
