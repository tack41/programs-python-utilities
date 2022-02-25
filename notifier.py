import pathlib
import json
import urllib
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class Notifier:

  __MAIL_SUBJECT_MAX_LENGTH = 50

  __use_slack = False
  __slack_webhook_url = ''
  def add_slack(self, slack_webhook_url: str):
    self.__use_slack = True
    self.__slack_webhook_url = slack_webhook_url

  def __slack(self,msg):
    params = {"text": msg}
    params_json = json.dumps(params)
    data = params_json.encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(self.__slack_webhook_url, data, headers)
    with urllib.request.urlopen(req) as res:
      body = res.read()
      result = body.decode("utf-8")


  __use_line = False
  __slack_webhook_url = ''
  def add_line(self, token: str):
    self.__use_line = True
    self.__line_token = token

  def __line(self,msg):
    method = "POST"
    headers = {"Authorization": f"Bearer {self.__line_token}"}

    payload = {"message": msg}
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
      url="https://notify-api.line.me/api/notify", data=payload, method=method, headers=headers)
    urllib.request.urlopen(req)


  __use_local_mta = False
  __local_mta_from_addr = ''
  __local_mta_to_addr = ''
  def add_local_mta(self, from_addr: str, to_addr: str):
    self.__use_local_mta = True
    self.__local_mta_from_addr = from_addr
    self.__local_mta_to_addr = to_addr

  def __local_mta(self,msg,attachment_path=None):
    mime_multi_part = MIMEMultipart()
    mime_multi_part.attach(MIMEText(msg))
    mime_multi_part["Subject"] = msg[:self.__MAIL_SUBJECT_MAX_LENGTH]
    mime_multi_part["To"] = self.__local_mta_to_addr
    mime_multi_part["From"] = self.__local_mta_from_addr
    if attachment_path is not None:
      with open(attachment_path, "rb") as f:
        mime_app = MIMEApplication(
          f.read(),
          Name=attachment_path.name
        )
      mime_app['Content-Disposition'] = f'attachment; filename="{attachment_path.name}"'
      mime_multi_part.attach(mime_app)

    server = smtplib.SMTP('localhost')
    server.send_message(mime_multi_part)
    server.quit()


  __use_gmail = False
  __gmail_from_addr = ''
  __gmail_to_addr = ''
  __gmail_id = ''
  __gmail_pw = ''
  def add_gmail(self, from_addr: str, to_addr: str, id: str, pw: str):
    self.__use_gmail = True
    self.__gmail_from_addr = from_addr
    self.__gmail_to_addr = to_addr
    self.__gmail_id = id
    self.__gmail_pw = pw

  def __gmail(self,msg,attachment_path=None):
    mime_multi_part = MIMEMultipart()
    mime_multi_part.attach(MIMEText(msg))
    mime_multi_part["Subject"] = msg[:self.__MAIL_SUBJECT_MAX_LENGTH]
    mime_multi_part["To"] = self.__gmail_to_addr
    mime_multi_part["From"] = self.__gmail_from_addr
    if attachment_path is not None:
      with open(attachment_path, "rb") as f:
        mime_app = MIMEApplication(
          f.read(),
          Name=attachment_path.name
        )
      mime_app['Content-Disposition'] = f'attachment; filename="{attachment_path.name}"'
      mime_multi_part.attach(mime_app)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(self.__gmail_id, self.__gmail_pw)
    server.send_message(mime_multi_part)
    server.quit()


  __use_external_mta_no_auth = False
  __external_mta_no_auth_smtp_server = ''
  __external_mta_no_auth_from_addr = ''
  __external_mta_no_auth_to_addr = ''
  def add_eternal_mta_no_auth(self, smtp_server: str, from_addr: str, to_addr: str):
    self.__use_external_mta_no_auth = True
    self.__external_mta_no_auth_smtp_server = smtp_server
    self.__external_mta_no_auth_from_addr = from_addr
    self.__external_mta_no_auth_to_addr = to_addr

  def __external_mta_no_auth(self,msg,attachment_path=None):
    mime_multi_part = MIMEMultipart()
    mime_multi_part.attach(MIMEText(msg))
    mime_multi_part["Subject"] = msg[:self.__MAIL_SUBJECT_MAX_LENGTH]
    mime_multi_part["To"] = self.__external_mta_no_auth_to_addr
    mime_multi_part["From"] = self.__external_mta_no_auth_from_addr
    if attachment_path is not None:
      with open(attachment_path, "rb") as f:
        mime_app = MIMEApplication(
          f.read(),
          Name=attachment_path.name
        )
      mime_app['Content-Disposition'] = f'attachment; filename="{attachment_path.name}"'
      mime_multi_part.attach(mime_app)

    server = smtplib.SMTP(__external_mta_no_auth_smtp_server, 25)
    server.send_message(mime_multi_part)
    server.quit()


  def send(self, msg: str, attachment_path: pathlib.Path=None):
    if self.__use_slack:
      self.__slack(msg)
    if self.__use_line:
      self.__line(msg)
    if self.__use_local_mta:
      self.__local_mta(msg,attachment_path)
    if self.__use_gmail:
      self.__gmail(msg,attachment_path)
    if self.__use_external_mta_no_auth:
      self.__external_mta_no_auth(msg,attachment_path)