import struct

import docker

from srsran_controller.common.docker.entity import Entity
from srsran_controller.common.ip import asyncio_udp_send_receive
from srsran_controller.common.ip import construct_forward
from srsran_controller.configuration import config
from srsran_controller.exceptions import EntityControlError


class Epc(Entity):
    CONTAINER_NAME = 'epc'
    CONF_CONTAINER_PATH = '/mnt/epc.conf'
    HSS_CONFIGURATION_PATH = '/mnt/user_db.csv'
    COMMAND = f'srsepc {CONF_CONTAINER_PATH}'
    TUN_CONTROL_PATH = '/dev/net/tun'
    LOG_CONTAINER_PATH = '/tmp/epc.log'
    CAP_CONTAINER_PATH = '/tmp/epc.pcap'
    CONTROL_PORT = 4567
    SGI_INTERFACE_NAME = 'srs_spgw_sgi'

    @staticmethod
    def create(configuration_path: str, hss_db: str):
        """
        Create a SrsEPC instance.
        :param configuration_path: SrsEPC configuration path.
        :param hss_db: SrsEPC users DB (HSS configuration) path.
        :return: Epc object.
        :rtype: Epc
        """
        client = docker.from_env()
        volumes = {
            configuration_path: {'bind': Epc.CONF_CONTAINER_PATH, 'mode': 'ro'},
            hss_db: {'bind': Epc.HSS_CONFIGURATION_PATH, 'mode': 'ro'},
            Epc.TUN_CONTROL_PATH: {'bind': Epc.TUN_CONTROL_PATH, 'mode': 'rw'},  # Allow creating TUN devices.
        }
        container = client.containers.create(
            config.epc_docker_image, Epc.COMMAND, volumes=volumes, cap_add=['NET_ADMIN'], auto_remove=True,
            name=Epc.CONTAINER_NAME, network_mode='none'
        )
        epc = Epc(container)
        epc._disconnect('none')
        return epc

    async def imsi_from_tmsi(self, tmsi: int) -> str:
        """
        Fetch an IMSI of a TMSI from the EPC.
        :param tmsi: Known TMSI.
        :return: IMSI if known, else empty string.
        """
        request = b'find_imsi_from_tmsi ' + struct.pack('<I', tmsi)
        response = await asyncio_udp_send_receive(request, self.ip, self.CONTROL_PORT)
        imsi, = struct.unpack('<Q', response)
        if not imsi:
            return ''
        return f'{imsi:015}'

    async def send_downlink_nas_transport(self, imsi: str, data: bytes) -> None:
        """
        Send downlink NAS transport.
        :param imsi: UE's IMSI.
        :param data: CP data to send.
        """
        request = b'send_downlink_nas_transport '
        request += struct.pack('<QB', int(imsi), len(data)) + data
        response = await asyncio_udp_send_receive(request, self.ip, self.CONTROL_PORT)
        if response != b'\x00':
            raise EntityControlError()

    async def send_downlink_generic_nas_transport(self, imsi: str, type_: int, data: bytes,
                                                  additional_information: bytes = b'') -> None:
        """
        Send downlink generic NAS transport.
        :param imsi: UE's IMSI.
        :param type_: Message container type. 1 for LPP, 2 for location service, etc.
        :param data: Message container data.
        :param additional_information: Message additional information.
        """
        request = b'send_downlink_generic_nas_transport '
        request += struct.pack('<QBH', int(imsi), type_, len(data)) + data
        request += struct.pack('<B', len(additional_information)) + additional_information
        response = await asyncio_udp_send_receive(request, self.ip, self.CONTROL_PORT)
        if response != b'\x00':
            raise EntityControlError()

    async def send_paging(self, imsi: str) -> None:
        """
        Send paging.
        :param imsi: UE's IMEI.
        """
        self.logger.info(f'Sending page to {imsi}')
        request = b'send_paging ' + struct.pack('<Q', int(imsi))
        response = await asyncio_udp_send_receive(request, self.ip, self.CONTROL_PORT)
        if response != b'\x00':
            raise EntityControlError()

    async def is_ecm_connected(self, imsi: str) -> bool:
        """
        Check that the imsi has active connection to the MME.
        :param imsi: UE's IMEI.
        """
        request = b'is_ecm_connected ' + struct.pack('<Q', int(imsi))
        response = await asyncio_udp_send_receive(request, self.ip, self.CONTROL_PORT)
        return bool(response[0])

    def ip_forward(self, network) -> None:
        """
        Forward ip transportation from the EPC to the specified network.
        :param network: Network to forward communication to.
        """
        out = network.INTERFACE_NAME + '0'  # Docker adds an index for bridges
        for iptable_command in construct_forward(self.SGI_INTERFACE_NAME, out):
            self._container.exec_run(iptable_command)
        self._container.exec_run(f'ip route replace default via {network.GATEWAY} dev {out}')
