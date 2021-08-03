import csv
from dataclasses import dataclass, fields

from srsran_controller.configuration import config

CSV_COLUMNS = ['name', 'auth', 'imsi', 'key', 'op_type', 'op', 'amf', 'sqn', 'qci', 'ip']


@dataclass
class Subscriber:
    index: int
    name: str
    imsi: str
    key: str
    op_type: str
    op: str
    amf: str
    sqn: int
    qci: int
    ip: str
    auth: str = 'mil'


class SubscribersManager:
    def iter_subscribers(self):
        with open(config.users_db) as subscribers_file:
            reader = csv.reader(subscribers_file)
            for i, row in enumerate(reader):
                data = {}
                for column_index, column in enumerate(CSV_COLUMNS):
                    field = next(f for f in fields(Subscriber) if f.name == column)
                    data[column] = field.type(row[column_index])
                yield Subscriber(i, **data)
