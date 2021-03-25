import docker

from srslte_controller.mission.lte_network import LteNetwork


def test_create():
    network = LteNetwork.create()
    client = docker.from_env()
    try:
        assert len(client.networks.list(names=[LteNetwork.NAME])) == 1
    finally:
        network.shutdown()


def test_shutdown():
    network = LteNetwork.create()
    network.shutdown()
    client = docker.from_env()
    assert len(client.networks.list(names=[LteNetwork.NAME])) == 0
