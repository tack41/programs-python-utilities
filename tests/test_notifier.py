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
    self.email_to_local = config_secret_ini.get('DEFAULT','email_to_local')
    self.email_from_gmail = config_secret_ini.get('DEFAULT','email_from_gmail')
    self.email_to_gmail = config_secret_ini.get('DEFAULT','email_to_gmail')
    self.email_id_gmail = config_secret_ini.get('DEFAULT','email_id_gmail')
    self.email_pw_gmail = config_secret_ini.get('DEFAULT','email_pw_gmail')
    self.email_from_ext_smtp = config_secret_ini.get('DEFAULT','email_from_ext_smtp')
    self.email_to_ext_smtp = config_secret_ini.get('DEFAULT','email_to_ext_smtp')
    self.email_smtp_server_ext_smtp = config_secret_ini.get('DEFAULT','email_smtp_server_ext_smtp')
    self.email_smtp_server_port_ext_smtp = config_secret_ini.getint('DEFAULT','email_smtp_server_port_ext_smtp')
    self.email_use_tls_ext_smtp = config_secret_ini.getboolean('DEFAULT','email_use_tls_ext_smtp')
    self.email_id_ext_smtp = config_secret_ini.get('DEFAULT','email_id_ext_smtp')
    self.email_pw_ext_smtp = config_secret_ini.get('DEFAULT','email_pw_ext_smtp')


config = Config()

attach_path = pathlib.Path(__file__) #テストに利用する添付ファイルはこのファイル自身を使用

class TestNotifier(unittest.TestCase):
  def test_slack_webhook(self):
    """Slack(webhook)通知"""

    if not config.slack_webhook_url:
      print("'slack_webhook_url' is not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_slack_webhook(config.slack_webhook_url)
    notifier.send("Slack(webhook) test","test message for slack(webhook)",attach_path)

    print("Check slack for a test message")
    self.assertTrue(True)


  def test_line(self):
    """LINE通知"""

    if not config.line_token:
      print("'config.line_token' is not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_line(config.line_token)
    notifier.send("LINE test","test message for line",attach_path)

    print("Check LINE for a test message")
    self.assertTrue(True)


  def test_email_local(self):
    """email通知(local)"""

    if (not config.email_from_local) or (not config.email_to_local):
      print("'config.email_from_local' or 'config.email_to_local' are not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_email(config.email_from_local,config.email_to_local)
    notifier.send("email(local) test","test message for mail(local)",attach_path)

    print(f"Check mail '{config.email_to_local}' for a test message")
    self.assertTrue(True)


  def test_email_by_gmail(self):
    """email通知(gmail)"""

    if (not config.email_from_gmail) or (not config.email_to_gmail) or (not config.email_id_gmail) or (not config.email_pw_gmail):
      print("'config.email_from_gmail' or 'config.email_to_gmail' or 'config.email_id_gmail' or 'config.email_pw_gmail' are not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_email(config.email_from_gmail,config.email_to_gmail,"smtp.gmail.com",587,config.email_id_gmail,config.email_pw_gmail,True)
    notifier.send("email(gmail) test","test message for mail(gmail)",attach_path)

    print(f"Check mail '{config.email_to_gmail}' for a test message")
    self.assertTrue(True)


  def test_email_by_external_smtp(self):
    """email通知(外部SMTP)"""

    if (not config.email_from_ext_smtp) or (not config.email_to_ext_smtp) or (not config.email_smtp_server_ext_smtp) or (not config.email_smtp_server_port_ext_smtp) or (not config.email_id_ext_smtp) or (not config.email_pw_ext_smtp):
      print("'config.email_from_ext_smtp' or 'config.email_to_ext_smtp' or 'config.email_smtp_server_ext_smtp' or 'config.email_smtp_server_port_ext_smtp' or 'config.email_id_ext_smtp' or 'config.email_pw_ext_smtp' are not defined. Skipping")
      return
    notifier = Notifier()
    notifier.add_email(config.email_from_ext_smtp,config.email_to_ext_smtp,config.email_smtp_server_ext_smtp,config.email_smtp_server_port_ext_smtp,config.email_id_ext_smtp,config.email_pw_ext_smtp,config.email_use_tls_ext_smtp)
    notifier.send("email(外部SMTP) test","test message for mail(外部SMTP)",attach_path)

    print(f"Check mail '{config.email_to_ext_smtp}' for a test message")
    self.assertTrue(True)


  def test_all(self):
    """slack(webhook),LINE,email(local)で送信"""

    notifier = Notifier()
    if not config.slack_webhook_url:
      print("'slack_webhook_url' is not defined. Skipping")
    else:
      notifier.add_slack_webhook(config.slack_webhook_url)

    if not config.line_token:
      print("'config.line_token' is not defined. Skipping")
    else:
      notifier.add_line(config.line_token)

    if (not config.email_from_local) or not (config.email_to_local):
      print("'config.email_from_local' or 'config.email_to_local' are not defined. Skipping")
    else:
      notifier.add_email(config.email_from_local,config.email_to_local)

    notifier.send("Slack(webhook,API),LINE,email(local,gmail) test","test message for Slack(webhook,API),LINE,email(local,gmail)")
    print(f"Check slack,email('{config.email_to_local}','{config.email_to_gmail}') for a test message")
    self.assertTrue(True)


  if __name__ == '__main__':
    unittest.main(verbosity=2)