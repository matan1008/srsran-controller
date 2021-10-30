import time
from contextlib import contextmanager
from ipaddress import IPv4Network
from tempfile import NamedTemporaryFile

from srsran_controller.mission.enb import Enb
from srsran_controller.mission.lte_network import LteNetwork
from srsran_controller.mission.mission_configuration import MissionConfiguration
from srsran_controller.mission_factory.enb import build_configuration, build_rr, build_rbs, build_sibs

ENB_SANITY_LOG = 'Setting frequency'


@contextmanager
def shutdown(instance):
    try:
        yield instance
    finally:
        instance.shutdown()


@contextmanager
def configuration_files(conf, epc_ip, enb_ip):
    enb_conf = NamedTemporaryFile(delete=True, mode='w')
    sibs = NamedTemporaryFile(delete=True, mode='w')
    rbs = NamedTemporaryFile(delete=True, mode='w')
    rr = NamedTemporaryFile(delete=True, mode='w')
    try:
        build_configuration(conf, epc_ip, enb_ip).write(enb_conf)
        enb_conf.flush()
        build_sibs(conf).write(sibs)
        sibs.flush()
        build_rbs().write(rbs)
        rbs.flush()
        build_rr(conf).write(rr)
        rr.flush()
        yield enb_conf.name, sibs.name, rbs.name, rr.name
    finally:
        enb_conf.close()
        sibs.close()
        rbs.close()
        rr.close()


@contextmanager
def launch_enb():
    epc_ip, enb_ip = map(str, list(IPv4Network(LteNetwork.SUBNET).hosts())[0:2])
    conf = MissionConfiguration(device_name='zmq')
    with configuration_files(conf, epc_ip, enb_ip) as config_files:
        enb_conf, sibs, rbs, rr = config_files
        with shutdown(LteNetwork.create()) as lte_network:
            with shutdown(Enb.create(enb_conf, sibs, rbs, rr)) as enb:
                enb.connect(lte_network, enb_ip)
                enb.start()
                enb.wait_for_ip()
                yield enb


def test_launching_enb():
    with launch_enb() as enb:
        # Wait for 30 seconds at most.
        for _ in range(30):
            if ENB_SANITY_LOG not in enb._container.logs().decode():
                time.sleep(1)
        assert ENB_SANITY_LOG in enb._container.logs().decode()
