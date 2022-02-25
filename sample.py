#!/usr/bin/env python3
import sys,os,subprocess
import pathlib
import argparse
import configparser
import logger
import notifier

if os.geteuid() != 0 or os.getuid() != 0 :
  print("このスクリプトの実行には、管理者権限が必要です。")
  sys.exit(1)

script_dir = pathlib.Path(__file__).parent.resolve()
script_name = pathlib.Path(__file__).name
script_name_stem = pathlib.Path(__file__).stem
parent_dir = script_dir.parent.resolve()

class Config:
  def __init__(self):
    config_ini = configparser.ConfigParser()
    config_ini.read(script_dir.joinpath('conf').joinpath('config.ini'), encoding='utf-8')
    self.gcs_bucket_name = config_ini.get('DEFAULT','setting1')

    config_secret_ini = configparser.ConfigParser()
    config_secret_ini.read(script_dir.joinpath('conf').joinpath('config_secret.ini'), encoding='utf-8')
    self.slack_webhook_url = config_secret_ini.get('DEFAULT','secret1')

config = Config()
log_dir = script_dir.joinpath("log")
if not log_dir.exists():
  os.makedirs(log_dir)
log_file = log_dir.joinpath(script_name_stem + ".log")

class Main():
  def run(self,verbose):

    logger = lib.logger.Logger(__name__, verbose, log_file)

    try:
      pass
      resultOK = True
      msg = 'error message'

      if(resultOK):
        logger.info("Succeeded")
        notifier.succeeded('Succeeded')
      else:
        logger.error(f"Failed: {msg}")
        notifier.failed("Failed: {msg}")

    except Exception as e:
      logger.exception(e)
      sys.exit(1)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--verbose", action="store_true")
  args = parser.parse_args()

  notifier = notifier.Notifier()
  notifier.add_slack('slack_webhook_url')
  notifier.add_line('line_token')
  notifier.add_local_mta('from@example.com','to@example.com')
  notifier.add_gmail('from@example.com','to@example.com','gmail_id','gmail_mail_pw')
  notifier.add_eternal_mta_no_auth('smtp.example.com','from@example.com','to@example.com')

  main = Main()
  (resultOK,msg) = main.run(args.verbose)

  if not resultOK:
    print(f"Some error occurred: {msg}")
    notifier.send(f"Failed to backup redmine: {msg}",log_file)
    sys.exit(1)
  else:
    print("Succcessfully completed")
    notifier.send("Succeeded to backup redmine",log_file)
    sys.exit(0)