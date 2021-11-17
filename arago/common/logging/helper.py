import logging, sys
from arago.common.logging.logger import Logger
from enum import Enum, auto


class Rotation(Enum):
	OFF = None
	HOURLY = 'H'
	DAILY = 'D'
	WEEKLY = 'W6'


def getCustomLogger(level="INFO", logfile=sys.stderr, formatting=None, rotation=Rotation.OFF):
	global logging
	logging.setLoggerClass(Logger)
	logger = logging.getLogger('top')
	level = getattr(logger, level)
	logger.setLevel(level)
	if formatting:
		formatter = logging.Formatter(*formatting)
	else:
		formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S")
	if logfile != sys.stderr:
		if rotation.value:
			import logging.handlers
			handler = logging.handlers.TimedRotatingFileHandler(logfile, when=rotation.value)
		else:
			handler = logging.FileHandler(logfile)
	elif logfile == sys.stderr:
		handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	handler.setLevel(level)
	for h in list(logger.handlers):
		if h.stream.name == handler.stream.name:
			logger.removeHandler(h)
	logger.addHandler(handler)
	return logger
