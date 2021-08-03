import csv
from dataclasses import dataclass, fields, asdict

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
    def create_subscriber(self, name, imsi, key, op_type, op, amf, sqn, qci, ip, auth='mil'):
        with open(config.users_db, 'a') as subscribers_file:
            writer = csv.writer(subscribers_file)
            writer.writerow([name, auth, imsi, key, op_type, op, amf, sqn, qci, ip])
        return list(self.iter_subscribers())[-1]

    @staticmethod
    def edit_subscriber(subscriber: Subscriber):
        with open(config.users_db) as subscribers_file:
            lines = list(csv.reader(subscribers_file))
        with open(config.users_db, 'w') as subscribers_file:
            writer = csv.writer(subscribers_file)
            for i, row in enumerate(lines):
                if i == subscriber.index:
                    writer.writerow([asdict(subscriber)[field] for field in CSV_COLUMNS])
                else:
                    writer.writerow(row)

    @staticmethod
    def delete_subscriber(subscriber: Subscriber):
        with open(config.users_db) as subscribers_file:
            lines = list(csv.reader(subscribers_file))
        with open(config.users_db, 'w') as subscribers_file:
            writer = csv.writer(subscribers_file)
            for i, row in enumerate(lines):
                if i == subscriber.index:
                    continue
                else:
                    writer.writerow(row)

    @staticmethod
    def iter_subscribers():
        with open(config.users_db) as subscribers_file:
            reader = csv.reader(subscribers_file)
            for i, row in enumerate(reader):
                data = {}
                for column_index, column in enumerate(CSV_COLUMNS):
                    field = next(f for f in fields(Subscriber) if f.name == column)
                    data[column] = field.type(row[column_index])
                yield Subscriber(i, **data)
