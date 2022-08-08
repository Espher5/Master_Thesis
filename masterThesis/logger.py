import logging
import os
from typing import Set

from folders import folders
from ini_file import IniFile


class Logger:
    def __init__(self):
        self._all_loggers: Set[logging.Logger] = set()
        self._log_ini: IniFile = None

    def use_ini(self, ini_path):
        self._log_ini = IniFile(ini_path)
        logging_format = self._log_ini.get_option_create_blank(
            'config', 'format', '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d] %(message)s'
        )
        logging_date_format = self._log_ini.get_option_create_blank(
            'config', 'date_format', '%H:%M:%S'
        )

        logging.basicConfig(format=logging_format, datefmt=logging_date_format)
        for log in self._all_loggers:
            self._setup_log_level(log)

    def _setup_log_level(self, log: logging.Logger):
        if self._log_ini:
            level = self._log_ini.get_option_create_blank('log_level', log.name, 'INFO')
        else:
            level = 'INFO'
        log.setLevel(level)

    def get_logger(self, logger_name_path):
        logger_name = os.path.basename(logger_name_path)
        log = logging.getLogger(logger_name)

        self._all_loggers.add(log)
        self._setup_log_level(log)
        return log


logger = Logger()
logger.use_ini(folders.log_ini)


def get_logger(logger_name_path):
    return logger.get_logger(logger_name_path)
