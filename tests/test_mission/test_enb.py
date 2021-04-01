import os
import time
from contextlib import contextmanager
from ipaddress import IPv4Network
from tempfile import NamedTemporaryFile

from srslte_controller.configuration import config
from srslte_controller.mission.enb import Enb
from srslte_controller.mission.lte_network import LteNetwork
from srslte_controller.mission.mission_configuration import MissionConfiguration
from srslte_controller.mission_factory.enb import build_configuration, build_rr, build_drbs, build_sibs

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
    drbs = NamedTemporaryFile(delete=True, mode='w')
    rr = NamedTemporaryFile(delete=True, mode='w')
    try:
        build_configuration(conf, epc_ip, enb_ip).write(enb_conf)
        enb_conf.flush()
        build_sibs(conf).write(sibs)
        sibs.flush()
        build_drbs().write(drbs)
        drbs.flush()
        build_rr(conf).write(rr)
        rr.flush()
        yield enb_conf.name, sibs.name, drbs.name, rr.name
    finally:
        enb_conf.close()
        sibs.close()
        drbs.close()
        rr.close()


@contextmanager
def launch_enb():
    epc_ip, enb_ip = map(str, list(IPv4Network(LteNetwork.SUBNET).hosts())[0:2])
    conf = MissionConfiguration()
    with configuration_files(conf, epc_ip, enb_ip) as config_files:
        enb_conf, sibs, drbs, rr = config_files
        with shutdown(LteNetwork.create()):
            with shutdown(Enb.create(enb_conf, sibs, drbs, rr, LteNetwork.NAME, enb_ip)) as enb:
                yield enb


def test_launching_enb():
    # Set the cap file to a file that doesn't exist.
    with NamedTemporaryFile(delete=True, mode='w+', suffix='.pcap') as tmp_cap:
        config.current_enb_cap = tmp_cap.name

    with launch_enb() as enb:
        # Wait for 5 seconds at most.
        for _ in range(5):
            if ENB_SANITY_LOG not in enb._container.logs().decode():
                time.sleep(1)
        assert ENB_SANITY_LOG in enb._container.logs().decode()


def test_launching_enb_cap_already_exists():
    tagged_data = 'not random data'
    # Set the cap file to a file that exists.
    with NamedTemporaryFile(delete=False, mode='w+', suffix='.pcap') as tmp_cap:
        tmp_cap.write(tagged_data)
        config.current_enb_cap = tmp_cap.name

    with launch_enb() as enb:
        # Wait for 5 seconds at most.
        for _ in range(5):
            if ENB_SANITY_LOG not in enb._container.logs().decode():
                time.sleep(1)
        assert ENB_SANITY_LOG in enb._container.logs().decode()

    # Make sure file was deleted
    assert not os.path.exists(config.current_enb_cap)
