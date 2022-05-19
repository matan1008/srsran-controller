import importlib.util
from logging import Logger, getLogger
from pathlib import Path


class ScriptsImporter:
    def __init__(self, scripts_folder: str, logger: Logger = getLogger('srsran_controller')):
        self.logger = logger
        self._scripts_folder = scripts_folder
        self._scripts_classes = {}

    def reload(self) -> None:
        """
        Reload the currently imported scripts.
        """
        self._scripts_classes.clear()
        for module in Path(self._scripts_folder).glob('*.py'):
            if not module.is_file():
                continue
            try:
                class_ = self._load_script_class_from_file(module)
                self._scripts_classes[class_.name] = class_
            except Exception:  # noqa
                self.logger.warning(f'Error loading script {module}')

    def get_scripts_names(self) -> list:
        """
        Return all the loaded scripts names.
        :return: Names of imported scripts.
        """
        return list(self._scripts_classes.keys())

    def get_script_class(self, name):
        """
        Get script class.
        :return: Script's class.
        :rtype: type[srsran_controller.scripts.abstract.AbstractScript]
        """
        return self._scripts_classes[name]

    def _load_script_class_from_file(self, file):
        """
        The file must contain a valid python code and a factory method name `get_script_class`.
        `get_script_class` mustn't have arguments and should return a subclass of AbstractScript.
        """
        spec = importlib.util.spec_from_file_location(file.stem, file)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m.get_script_class()
