import sys,os,subprocess
import pathlib
import unittest
import configparser

script_dir = pathlib.Path(__file__).parent.resolve()
script_name = pathlib.Path(__file__).name
script_name_stem = pathlib.Path(__file__).stem
parent_dir = script_dir.parent.resolve()

sys.path.append(str(parent_dir))
from notifier import Notifier

class Config:
  def __init__(self):
    config_secret_ini = configparser.ConfigParser()
    config_secret_ini.read(script_dir.joinpath('conf').joinpath('config_secret.ini'), encoding='utf-8')
    self.slack_webhook_url = config_secret_ini.get('DEFAULT','slack_webhook_url')
    self.line_token = config_secret_ini.get('DEFAULT','line_token')
    self.local_mta_from_addr = config_secret_ini.get('DEFAULT','local_mta_from_addr')
    self.local_mta_to_addr = config_secret_ini.get('DEFAULT','local_mta_to_addr')
    self.gmail_from_addr = config_secret_ini.get('DEFAULT','gmail_from_addr')
    self.gmail_to_addr = config_secret_ini.get('DEFAULT','gmail_to_addr')
    self.gmail_id = config_secret_ini.get('DEFAULT','gmail_id')
    self.gmail_pw = config_secret_ini.get('DEFAULT','gmail_pw')

config = Config()

class TestNotifier(unittest.TestCase):
  def test_slack(self):
    """Slack通知のみ"""

    notifier = Notifier()
    notifier.add_slack(config.slack_webhook_url)
    notifier.send("test message for slack")

    print("Check slack for a test message")
    self.assertTrue(True)


  def test_line(self):
    """LINE通知のみ"""

    notifier = Notifier()
    notifier.add_line(config.line_token)
    notifier.send("test message for line")

    print("Check LINE for a test message")
    self.assertTrue(True)


  def test_local_mta(self):
    """localhost:25へのメールのみ"""

    notifier = Notifier()
    notifier.add_local_mta(config.local_mta_from_addr, config.local_mta_to_addr)
    notifier.send("test message for local mta",pathlib.Path(__file__))

    print(f"Check Mail '{config.local_mta_to_addr}' for a test message")
    self.assertTrue(True)


  def test_gmail(self):
    """gmailのみ"""

    notifier = Notifier()
    notifier.add_gmail(config.local_mta_from_addr, config.local_mta_to_addr, config.gmail_id, config.gmail_pw)
    notifier.send("test message for local mta",pathlib.Path(__file__))

    print(f"Check Mail '{config.local_mta_to_addr}' for a test message")
    self.assertTrue(True)


  def test_all(self):
    """slack,LINE,local_mta,gmailで送信"""

    notifier = Notifier()
    notifier.add_slack(config.slack_webhook_url)
    notifier.add_line(config.line_token)
    notifier.add_local_mta(config.local_mta_from_addr, config.local_mta_to_addr)
    notifier.add_gmail(config.local_mta_from_addr, config.local_mta_to_addr, config.gmail_id, config.gmail_pw)
    notifier.send("test message for slack,LINE,local_mta,gmail",pathlib.Path(__file__))

    print(f"Check slack,LINE,local_mta({config.local_mta_to_addr  }),gmail({config.gmail_to_addr}) for a test message")
    self.assertTrue(True)


  if __name__ == '__main__':
    unittest.main(verbosity=2)