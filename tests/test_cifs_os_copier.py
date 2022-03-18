import sys,os,subprocess
import pathlib
import unittest
import configparser

script_dir = pathlib.Path(__file__).parent.resolve()
script_name = pathlib.Path(__file__).name
script_name_stem = pathlib.Path(__file__).stem
parent_dir = script_dir.parent.resolve()

sys.path.append(str(parent_dir))
from cifs_os_copier import CIFSOSCopier

class Config:
  def __init__(self):
    config_secret_ini = configparser.ConfigParser()
    config_secret_ini.read(script_dir.joinpath('conf').joinpath('config_secret.ini'), encoding='utf-8')
    self.cifs_domain_name = config_secret_ini.get('DEFAULT','cifs_domain_name')
    self.cifs_remote_cifs_dir = config_secret_ini.get('DEFAULT','cifs_remote_cifs_dir')
    self.cifs_local_mount_dir = config_secret_ini.get('DEFAULT','cifs_local_mount_dir')
    self.cifs_id = config_secret_ini.get('DEFAULT','cifs_id')
    self.cifs_pw = config_secret_ini.get('DEFAULT','cifs_pw')
    self.cifs_copy_from = config_secret_ini.get('DEFAULT','cifs_copy_from')
    self.cifs_copy_to = config_secret_ini.get('DEFAULT','cifs_copy_to')

config = Config()

class TestNotifier(unittest.TestCase):
  def test_copy(self):
    """CIFSOSCopier.copy"""

    with CIFSOSCopier(config.cifs_domain_name,config.cifs_remote_cifs_dir,pathlib.Path(config.cifs_local_mount_dir),config.cifs_id,config.cifs_pw) as cifsoscopier:
      cifsoscopier.copy([pathlib.Path(config.cifs_copy_from)],pathlib.Path(config.cifs_copy_to))

    self.assertTrue(True)


if __name__ == '__main__':
  unittest.main(verbosity=2)