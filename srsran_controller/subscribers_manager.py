import csv
from dataclasses import dataclass

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
            writer = csv.writer(subscribers_file, lineterminator='\n')
            writer.writerow([name, auth, imsi, key, op_type, op, amf, f'{sqn:012x}', qci, ip])
        return list(self.iter_subscribers())[-1]

    def edit_subscriber(self, subscriber: Subscriber):
        lines = list(self._iter_db_lines())
        with open(config.users_db, 'w') as subscribers_file:
            writer = csv.writer(subscribers_file, lineterminator='\n')
            for i, row in enumerate(lines):
                if i == subscriber.index:
                    writer.writerow([
                        subscriber.name, subscriber.auth, subscriber.imsi, subscriber.key, subscriber.op_type,
                        subscriber.op, subscriber.amf, f'{subscriber.sqn:012x}', subscriber.qci, subscriber.ip
                    ])
                else:
                    writer.writerow(row)

    def delete_subscriber(self, subscriber: Subscriber):
        lines = list(self._iter_db_lines())
        with open(config.users_db, 'w') as subscribers_file:
            writer = csv.writer(subscribers_file, lineterminator='\n')
            for i, row in enumerate(lines):
                if i == subscriber.index:
                    continue
                else:
                    writer.writerow(row)

    def iter_subscribers(self):
        for i, row in enumerate(self._iter_db_lines()):
            # The row is in the following format: Name,Auth,IMSI,Key,OP_Type,OP/OPc,AMF,SQN,QCI,IP_alloc
            yield Subscriber(i, row[0], row[2], row[3], row[4], row[5], row[6], int(row[7], 16), int(row[8]), row[9],
                             row[1])

    @staticmethod
    def _iter_db_lines():
        with open(config.users_db) as subscribers_file:
            reader = csv.reader(filter(lambda line: line[0] != '#', subscribers_file))
            for row in reader:
                yield row
