import logging, sys
from arago.common.logging.logger import Logger


def getCustomLogger(level="INFO", logfile=sys.stderr, formatting=None):
	logging.setLoggerClass(Logger)
	logger = logging.getLogger('root')
	level = getattr(logger, level)
	logger.setLevel(level)
	if formatting:
		formatter = logging.Formatter(*formatting)
	else:
		formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S")
	if logfile != sys.stderr:
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
