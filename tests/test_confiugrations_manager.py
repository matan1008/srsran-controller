import json
from dataclasses import asdict

import pytest

from srslte_controller.configurations_manager import ConfigurationsManager
from srslte_controller.exceptions import MissionIdNotFoundError
from srslte_controller.mission.mission_configuration import MissionConfiguration


def test_create_mission(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()

    files = list(tmpdir.listdir())
    assert len(files) == 1
    assert files[0].basename == conf.id

    with open(files[0], 'r') as fd:
        assert json.load(fd) == asdict(conf)


def test_get_mission(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    assert conf == configuration_manager.get_mission(conf.id)


def test_get_mission_error(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    with pytest.raises(MissionIdNotFoundError):
        assert configuration_manager.get_mission('mission_that_doesnt_exist')


def test_update_mission(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    conf.mnc = '02'
    configuration_manager.update_mission(conf)

    with open(tmpdir.listdir()[0], 'r') as fd:
        assert json.load(fd) == asdict(conf)


def test_update_mission_error(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = MissionConfiguration()
    with pytest.raises(MissionIdNotFoundError):
        assert configuration_manager.update_mission(conf)


def test_delete_mission(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf1 = configuration_manager.create_mission()
    conf2 = configuration_manager.create_mission()
    configuration_manager.delete_mission(conf2.id)

    files = list(tmpdir.listdir())
    assert len(files) == 1
    assert files[0].basename == conf1.id


def test_delete_mission_error(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    with pytest.raises(MissionIdNotFoundError):
        assert configuration_manager.delete_mission('mission_that_doesnt_exist')
