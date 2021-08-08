import pytest

from srsran_controller.configuration import config
from srsran_controller.subscribers_manager import SubscribersManager, Subscriber


@pytest.fixture(scope='function', autouse=True)
def users_db_file(tmp_path):
    old_users = config.users_db
    config.users_db = (tmp_path / 'new_db.csv').absolute()
    try:
        yield config.users_db
    finally:
        config.users_db = old_users


def test_adding_subscribers(users_db_file):
    s = SubscribersManager()
    sub = s.create_subscriber('Name', '001010123456785', '00112233445566778899aabbccddeeff', 'opc',
                              '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    assert sub.index == 0
    assert sub.name == 'Name'
    assert sub.imsi == '001010123456785'
    assert sub.key == '00112233445566778899aabbccddeeff'
    assert sub.op_type == 'opc'
    assert sub.op == '63bfa50ee6523365ff14c1f45f88737d'
    assert sub.amf == '9001'
    assert sub.sqn == 1233
    assert sub.qci == 9
    assert sub.ip == 'dynamic'
    assert sub.auth == 'mil'
    assert users_db_file.read_text() == ('Name,mil,001010123456785,00112233445566778899aabbccddeeff,opc,'
                                         '63bfa50ee6523365ff14c1f45f88737d,9001,0000000004d1,9,dynamic\n')


def test_deleting_subscribers(users_db_file):
    s = SubscribersManager()
    sub = s.create_subscriber('Name', '001010123456785', '00112233445566778899aabbccddeeff', 'opc',
                              '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    sub2 = s.create_subscriber('Name2', '001010123456783', '00112233445566778899aabbccddeeff', 'opc',
                               '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    s.delete_subscriber(sub)
    assert users_db_file.read_text() == ('Name2,mil,001010123456783,00112233445566778899aabbccddeeff,opc,'
                                         '63bfa50ee6523365ff14c1f45f88737d,9001,0000000004d1,9,dynamic\n')
    sub2.index -= 1
    s.delete_subscriber(sub2)
    assert not users_db_file.read_text()


def test_iterating_subscribers():
    s = SubscribersManager()
    sub = s.create_subscriber('Name', '001010123456785', '00112233445566778899aabbccddeeff', 'opc',
                              '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    sub2 = s.create_subscriber('Name2', '001010123456783', '00112233445566778899aabbccddeeff', 'opc',
                               '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    assert [sub, sub2] == list(s.iter_subscribers())


def test_iterating_subscribers_with_comment(users_db_file):
    users_db_file.write_text(
        '# Name,mil,001010123456785,00112233445566778899aabbccddeeff,opc,63bfa50ee6523365ff14c1f45f88737d,9001,1233,9,'
        'dynamic\n'
        'Name2,mil,001010123456783,00112233445566778899aabbccddeeff,opc,63bfa50ee6523365ff14c1f45f88737d,9001,1233,9,'
        'dynamic\n'
    )
    s = SubscribersManager()
    assert list(s.iter_subscribers()) == [Subscriber(
        0, 'Name2', '001010123456783', '00112233445566778899aabbccddeeff', 'opc', '63bfa50ee6523365ff14c1f45f88737d',
        '9001', 4659, 9, 'dynamic'
    )]


def test_editing_subscribers(users_db_file):
    s = SubscribersManager()
    sub = s.create_subscriber('Name', '001010123456785', '00112233445566778899aabbccddeeff', 'opc',
                              '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    s.create_subscriber('Name2', '001010123456783', '00112233445566778899aabbccddeeff', 'opc',
                        '63bfa50ee6523365ff14c1f45f88737d', '9001', 1233, 9, 'dynamic')
    sub.name = 'New Name!'
    s.edit_subscriber(sub)
    assert users_db_file.read_text() == (
        'New Name!,mil,001010123456785,00112233445566778899aabbccddeeff,opc,63bfa50ee6523365ff14c1f45f88737d,9001,'
        '0000000004d1,9,dynamic\n'
        'Name2,mil,001010123456783,00112233445566778899aabbccddeeff,opc,63bfa50ee6523365ff14c1f45f88737d,9001,'
        '0000000004d1,9,dynamic\n'
    )
