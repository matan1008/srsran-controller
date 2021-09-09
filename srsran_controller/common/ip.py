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
