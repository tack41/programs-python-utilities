import sys
import logging,logging.handlers
import pathlib

class Logger:
  def __init__(self, name: str=None, verbose=False, log_file: pathlib.Path=None):

    self.__logger = logging.getLogger(__name__ if name is None else name)
    self.__logger.setLevel(logging.DEBUG)
    self.__logger.propagate = False
    log_format = logging.Formatter("%(asctime)s [%(levelname)8s] %(message)s")

    # Log level less than WARNING to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_format)
    if verbose:
      stdout_handler.setLevel(logging.DEBUG)
    else:
      stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.WARNING)
    self.__logger.addHandler(stdout_handler)

    # Log level ERROR to stdout
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(log_format)
    stderr_handler.setLevel(logging.ERROR)
    self.__logger.addHandler(stderr_handler)

    # All log level to file output
    if log_file is not None:
      file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file,
        encoding='UTF-8',
        when='MIDNIGHT',
        backupCount=7)
      file_handler.setFormatter(log_format)
      file_handler.setLevel(logging.DEBUG)
      self.__logger.addHandler(file_handler)
  
  def debug(self,msg):
    self.__logger.debug(msg)
  def info(self,msg):
    self.__logger.info(msg)
  def warning(self,msg):
    self.__logger.warning(msg)
  def error(self,msg):
    self.__logger.error(msg)
  def critical(self,msg):
    self.__logger.critical(msg)
  def exception(self,e):
    self.__logger.exception(e)