import datetime
import json
from logging import getLogger, Logger
from pathlib import Path

from srsran_controller.exceptions import MissionIdNotFoundError


class Products:
    def __init__(self, products_folder: Path | str, logger: Logger = getLogger('srsran_controller')):
        self.products_folder = Path(products_folder)
        self.logger = logger
        self.output_fd = None
        self.products_folder.mkdir(exist_ok=True, parents=True)

    def set_mission(self, mission):
        """
        :param srsran_controller.mission.mission.Mission mission:
        """
        self.close()
        self.output_fd = open(self.products_folder / f'{mission.id}.ndjson', 'w')
        self.write_mission(mission)

    def write_mission(self, mission):
        """
        :param srsran_controller.mission.mission.Mission mission:
        """
        self._write('mission', {
            'id': mission.id,
            'time': mission.start_time.timestamp(),
        })

    def write_event(self, event: dict):
        jsonable_event = event.copy()
        jsonable_event['time'] = jsonable_event['time'].timestamp()
        self._write('event', jsonable_event)

    def close(self):
        if self.output_fd is None:
            return
        self.output_fd.close()
        self.output_fd = None

    def list_missions(self):
        missions = []
        for mission, _ in self._iter_missions():
            missions.append(mission)
        return missions

    def get_events(self, mission_id):
        events = []
        for product in self._mission_products(mission_id):
            if product['type'] != 'event':
                continue
            product['data']['time'] = datetime.datetime.fromtimestamp(product['data']['time'])
            events.append(product['data'])
        return events

    def _write(self, type_, data):
        self.output_fd.write(json.dumps({
            'type': type_,
            'data': data,
        }) + '\n')
        self.output_fd.flush()

    def _iter_missions(self):
        for f in filter(lambda p: p.is_file(), self.products_folder.iterdir()):
            try:
                with open(f, 'r') as fd:
                    data = json.loads(fd.readline())
                if data['type'] != 'mission':
                    self.logger.warning(f'No mission entry in product {f.name}')
                    continue
                yield data['data'], f
            except json.JSONDecodeError:
                self.logger.warning(f'Could not decode {f.name} in products folder')

    def _mission_products(self, mission_id):
        for mission, file in self._iter_missions():
            if mission['id'] == mission_id:
                break
        else:
            raise MissionIdNotFoundError()
        with open(file, 'r') as fd:
            for line in fd.readlines():
                try:
                    product = json.loads(line)
                except json.JSONDecodeError:
                    self.logger.warning(f'Could not decode {file.name} in products folder')
                    return
                yield product
