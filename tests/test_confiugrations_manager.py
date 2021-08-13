import json
from dataclasses import asdict
from uuid import uuid4

import pytest

from srsran_controller.configurations_manager import ConfigurationsManager
from srsran_controller.exceptions import MissionIdNotFoundError
from srsran_controller.mission.mission_configuration import MissionConfiguration, GsmNeighbor, EnbCell


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


def test_list_missions(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    configuration_manager.create_mission()
    configuration_manager.create_mission()
    assert len(configuration_manager.list_missions()) == 2


def test_mission_with_gsm_neighbor(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    conf.gsm_neighbors = [GsmNeighbor(arfcn=871, band='dcs1800')]
    configuration_manager.update_mission(conf)
    assert configuration_manager.get_mission(conf.id).gsm_neighbors[0].arfcn == conf.gsm_neighbors[0].arfcn
    assert configuration_manager.get_mission(conf.id).gsm_neighbors[0].band == conf.gsm_neighbors[0].band


def test_updating_all_configuration_values(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    conf.name = 'Old mission'
    conf.mcc = '901'
    conf.mnc = '01'
    conf.mme_code = '0x1b'
    conf.mme_group = '0x0002'
    conf.tac = 9
    conf.apn = 'inter'
    conf.full_net_name = 'new full'
    conf.short_net_name = 'new short'
    conf.gsm_neighbors = [GsmNeighbor(arfcn=871, band='dcs1800')]
    conf.cells = [EnbCell(), EnbCell(pci=2, cell_id=2, earfcn=1500)]
    conf.device_name = 'auto'
    conf.device_args = 'serial=33333333'
    conf.enb_id = 0x19a
    configuration_manager.update_mission(conf)
    conf = configuration_manager.get_mission(conf.id)

    assert conf.name == 'Old mission'
    assert conf.mcc == '901'
    assert conf.mnc == '01'
    assert conf.mme_code == '0x1b'
    assert conf.mme_group == '0x0002'
    assert conf.tac == 9
    assert conf.apn == 'inter'
    assert conf.full_net_name == 'new full'
    assert conf.short_net_name == 'new short'
    assert conf.gsm_neighbors == [GsmNeighbor(arfcn=871, band='dcs1800')]
    assert conf.cells == [EnbCell(), EnbCell(pci=2, cell_id=2, earfcn=1500)]
    assert conf.device_name == 'auto'
    assert conf.device_args == 'serial=33333333'
    assert conf.enb_id == 0x19a


def test_invalid_mission_format(tmpdir):
    with open(tmpdir / str(uuid4()), 'w') as fd:
        fd.write('Not a valid JSON {{{')
    configuration_manager = ConfigurationsManager(tmpdir)
    mission = configuration_manager.create_mission()
    assert configuration_manager.list_missions() == [mission]


def test_invalid_mission_fields(tmpdir):
    mission = asdict(MissionConfiguration())
    mission['not_enb_id'] = mission['enb_id']
    del mission['enb_id']
    with open(tmpdir / mission['id'], 'w') as fd:
        json.dump(mission, fd, indent=4)
    configuration_manager = ConfigurationsManager(tmpdir)
    mission = configuration_manager.create_mission()
    assert configuration_manager.list_missions() == [mission]
