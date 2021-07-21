import asyncio

import netifaces

from srsran_controller.common.utils import run_as_sudo


def construct_iptables_append(chain, jump, table='', in_='', out='', state=''):
    command = ['iptables']
    if table:
        command.extend(['-t', table])
    command.extend(['-A', chain])
    if in_:
        command.extend(['-i', in_])
    if out:
        command.extend(['-o', out])
    if state:
        command.extend(['-m', 'state', '--state', state])
    command.extend(['-j', jump])
    return command


def construct_forward(from_, to):
    return [
        construct_iptables_append('FORWARD', 'ACCEPT', in_=from_, out=to),
        construct_iptables_append('FORWARD', 'ACCEPT', in_=to, out=from_, state='ESTABLISHED,RELATED'),
        construct_iptables_append('POSTROUTING', 'MASQUERADE', out=to, table='nat'),
    ]


def forward_interfaces(from_, to, password):
    for iptable_command in construct_forward(from_, to):
        run_as_sudo(iptable_command, password)


class UdpSendReceiveProtocol(asyncio.DatagramProtocol):
    def __init__(self, message, on_receive):
        self.message = message
        self.on_receive = on_receive
        self.transport = None

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport
        self.transport.sendto(self.message)

    def datagram_received(self, data, addr):
        self.on_receive.set_result(data)
        self.transport.close()


async def asyncio_udp_send_receive(data, ip, port):
    loop = asyncio.get_running_loop()
    on_receive = loop.create_future()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpSendReceiveProtocol(data, on_receive),
        remote_addr=(ip, port))
    try:
        return await on_receive
    finally:
        transport.close()


def find_interface_of_address(ip_address):
    for interface in netifaces.interfaces():
        for addr in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
            if addr['addr'] == ip_address:
                return interface
