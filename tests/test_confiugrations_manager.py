import json
from dataclasses import asdict
from uuid import uuid4

import pytest

from srsran_controller.configurations_manager import ConfigurationsManager
from srsran_controller.exceptions import MissionIdNotFoundError
from srsran_controller.mission.mission_configuration import MissionConfiguration, GsmNeighbour, EnbCell, \
    IntraFreqNeighbour, WlanAssisted


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


def test_mission_with_gsm_neighbour(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    conf.gsm_neighbours = [GsmNeighbour(arfcn=871, band='dcs1800')]
    configuration_manager.update_mission(conf)
    assert configuration_manager.get_mission(conf.id).gsm_neighbours[0].arfcn == conf.gsm_neighbours[0].arfcn
    assert configuration_manager.get_mission(conf.id).gsm_neighbours[0].band == conf.gsm_neighbours[0].band


def test_mission_with_intra_feq_neighbours(tmpdir):
    configuration_manager = ConfigurationsManager(tmpdir)
    conf = configuration_manager.create_mission()
    conf.intra_freq_neighbours = [IntraFreqNeighbour(phys_cell_id=10, q_offset_cell=5)]
    configuration_manager.update_mission(conf)
    mission = configuration_manager.get_mission(conf.id)
    assert mission.intra_freq_neighbours[0].phys_cell_id == conf.intra_freq_neighbours[0].phys_cell_id
    assert mission.intra_freq_neighbours[0].q_offset_cell == conf.intra_freq_neighbours[0].q_offset_cell


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
    conf.gsm_neighbours = [GsmNeighbour(arfcn=871, band='dcs1800')]
    conf.intra_freq_neighbours = [IntraFreqNeighbour(phys_cell_id=10, q_offset_cell=5)]
    conf.wlan_assisted = [WlanAssisted(ssid='yooooo')]
    conf.cells = [EnbCell(), EnbCell(pci=2, cell_id=2, earfcn=1500, device_name='auto', device_args='serial=33333333')]
    conf.enb_id = 0x19a
    conf.external_interface = 'new external interface'
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
    assert conf.gsm_neighbours == [GsmNeighbour(arfcn=871, band='dcs1800')]
    assert conf.intra_freq_neighbours == [IntraFreqNeighbour(phys_cell_id=10, q_offset_cell=5)]
    assert conf.wlan_assisted == [WlanAssisted(ssid='yooooo')]
    assert conf.cells == [EnbCell(),
                          EnbCell(pci=2, cell_id=2, earfcn=1500, device_name='auto', device_args='serial=33333333')]
    assert conf.enb_id == 0x19a
    assert conf.external_interface == 'new external interface'


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
