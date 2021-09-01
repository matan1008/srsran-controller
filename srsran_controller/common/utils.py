from contextlib import contextmanager
from subprocess import Popen, PIPE


@contextmanager
def shutdown_on_error(instance):
    try:
        yield instance
    except Exception:
        instance.shutdown()
        raise


def run_as_sudo(command, password, stdout=PIPE, stderr=PIPE):
    sudo = ['sudo', '-S'] + command
    with Popen(sudo, stdin=PIPE, stdout=stdout, stderr=stderr) as proc:
        proc.communicate(password.encode())
