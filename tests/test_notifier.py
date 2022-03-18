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
    self.email_from_local = config_secret_ini.get('DEFAULT','email_from_local')
    self.email_to_addr = config_secret_ini.get('DEFAULT','email_to_local')

config = Config()

class TestNotifier(unittest.TestCase):
  def test_slack(self):
    """Slack通知"""

    if not config.slack_webhook_url:
      print("'slack_webhook_url' is not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_slack(config.slack_webhook_url)
    notifier.send("Slack test","test message for slack")

    print("Check slack for a test message")
    self.assertTrue(True)


  def test_line(self):
    """LINE通知"""

    if not config.config.line_token:
      print("'config.line_token' is not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_line(config.line_token)
    notifier.send("LINE test","test message for line")

    print("Check LINE for a test message")
    self.assertTrue(True)


""""
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
"""

  def test_mail_local(self):
    """email通知(local)"""

    if (not config.config.email_from_local) or not (config.config.email_to_local):
      print("'config.email_from_local' or 'config.email_to_local' are not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_email(config.email_from_local,config.email_to_local)
    notifier.send("test message for mail(local)")

    print(f"Check mail '{config.email_to_local}' for a test message")
    self.assertTrue(True)

  def test_all(self):
    """slack,LINE,email(local)で送信"""

    notifier = Notifier()
    if not config.slack_webhook_url:
      print("'slack_webhook_url' is not defined. Skipping")
    else:
      notifier.add_slack(config.slack_webhook_url)

    if not config.config.line_token:
      print("'config.line_token' is not defined. Skipping")
    else:
      notifier.add_line(config.line_token)

    if (not config.config.email_from_local) or not (config.config.email_to_local):
      print("'config.email_from_local' or 'config.email_to_local' are not defined. Skipping")
    else:
      notifier.add_email(config.email_from_local,config.email_to_local)

    print(f"Check slack,email(local({config.email_to_local})) for a test message")
    self.assertTrue(True)


  if __name__ == '__main__':
    unittest.main(verbosity=2)