import sys,os,subprocess
import pathlib
import unittest

script_dir = pathlib.Path(__file__).parent.resolve()
script_name = pathlib.Path(__file__).name
script_name_stem = pathlib.Path(__file__).stem
parent_dir = script_dir.parent.resolve()

sys.path.append(str(parent_dir))
from logger import Logger

class TestLogger(unittest.TestCase):
  def test_without_file_no_verbose(self):
    """ファイル出力なし,冗長出力なし"""

    logger = Logger(sys._getframe().f_code.co_name)

    print("")
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    try:
      zde = 1 / 0
    except ZeroDivisionError as e:
      logger.exception(e)

    print("---Check the 5 lines 'info','warning','error','critical','error' and stack traces are displayed")
    self.assertTrue(True)
    return 0


  def test_without_file_verbose(self):
    """ファイル出力なし,冗長出力あり"""
    
    logger = Logger(sys._getframe().f_code.co_name,True)

    print("")
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    try:
      zde = 1 / 0
    except ZeroDivisionError as e:
      logger.exception(e)

    print("---Check the 6 lines 'debug','info','warning','error','critical','error' and stack traces are displayed")
    self.assertTrue(True)


  def test_with_file_no_verbose(self):
    """ファイル出力あり,冗長出力なし"""

    log_file = script_dir.joinpath("result1.log")
    if log_file.exists():
      os.remove(log_file)

    logger = Logger(sys._getframe().f_code.co_name, False, log_file)

    print("")
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    try:
      zde = 1 / 0
    except ZeroDivisionError as e:
      logger.exception(e)

    rc = subprocess.call(f"grep -c debug {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c info {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c warning {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c error {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c critical {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c Traceback {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    print("---Check the 5 lines 'info','warning','error','critical','error' and stack traces are displayed")
    self.assertTrue(True)


  def test_with_file_verbose(self):
    """ファイル出力あり,冗長出力あり"""

    log_file = script_dir.joinpath("result2.log")
    if log_file.exists():
      os.remove(log_file)

    logger = Logger(sys._getframe().f_code.co_name, True, log_file)

    print("")
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    try:
      zde = 1 / 0
    except ZeroDivisionError as e:
      logger.exception(e)

    rc = subprocess.call(f"grep -c debug {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c info {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c warning {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c error {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c critical {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    rc = subprocess.call(f"grep -c Traceback {log_file} | grep -E '^1$'", shell=True, stdout=subprocess.DEVNULL)
    self.assertEqual(0, rc)

    print("---Check the 6 lines 'debug','info','warning','error','critical','error' and stack traces are displayed")
    self.assertTrue(True)


  if __name__ == '__main__':
    unittest.main(verbosity=2)