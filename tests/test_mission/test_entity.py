import docker
import pytest
from docker.errors import NotFound

from srsran_controller.mission.entity import Entity

TEST_IMAGE_DOCKER = 'ubuntu'
TEST_COMMAND = '/bin/yes'


@pytest.fixture(scope='function')
def container():
    client = docker.from_env()
    return client.containers.run(TEST_IMAGE_DOCKER, TEST_COMMAND, auto_remove=True, detach=True)


def test_shutting_down(container):
    client = docker.from_env()
    entity = Entity(container)
    entity.shutdown()
    with pytest.raises(NotFound):
        assert client.containers.get(container.id)


def test_shutting_down_removed_container(container):
    client = docker.from_env()
    entity = Entity(container)
    container.kill()
    container.wait(condition='removed')
    entity.shutdown()
    with pytest.raises(NotFound):
        assert client.containers.get(container.id)
