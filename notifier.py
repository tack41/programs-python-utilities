import pathlib
import json
import urllib
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class Notifier:

  __MAIL_SUBJECT_MAX_LENGTH = 100

  __use_slack_webhook = False
  __slack_webhook_url = ''
  def add_slack_webhook(self, slack_webhook_url: str):
    self.__use_slack_webhook = True
    self.__slack_webhook_url = slack_webhook_url

  def __slack_webhook(self,subject,body):
    params = {"text": f"{subject}\n{body}"}
    params_json = json.dumps(params)
    data = params_json.encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(self.__slack_webhook_url, data, headers)
    with urllib.request.urlopen(req) as res:
      body = res.read()
      result = body.decode("utf-8")
      print(result)


  __use_line = False
  __line_token = ''
  def add_line(self, token: str):
    self.__use_line = True
    self.__line_token = token

  def __line(self,subject,body):
    method = "POST"
    headers = {"Authorization": f"Bearer {self.__line_token}"}

    payload = {"message": f"{subject}\n{body}"}
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
      url="https://notify-api.line.me/api/notify", data=payload, method=method, headers=headers)
    urllib.request.urlopen(req)


  __use_email = False
  __email_from_addr = ''
  __email_to_addr = ''
  __email_smtp_server = ''
  __email_smtp_server_port = 0
  __email_auth_id = ''
  __email_auth_pw = ''
  __email_use_tls = True
  def add_email(self, from_addr: str, to_addr: str, smtp_server: str="localhost", smtp_server_port: int=25, auth_id: str='', auth_pw: str='', use_tls: bool=False):
    self.__use_email = True
    self.__email_from_addr = from_addr
    self.__email_to_addr = to_addr
    self.__email_smtp_server = smtp_server
    self.__email_smtp_server_port = smtp_server_port
    self.__email_auth_id = auth_id
    self.__email_auth_pw = auth_pw
    self.__email_use_tls = use_tls

  def __email(self,subject,body,attachment_path=None):
    mime_multi_part = MIMEMultipart()
    mime_multi_part.attach(MIMEText(body))
    mime_multi_part["Subject"] = subject[:self.__MAIL_SUBJECT_MAX_LENGTH]
    mime_multi_part["To"] = self.__email_to_addr
    mime_multi_part["From"] = self.__email_from_addr
    if attachment_path is not None:
      with open(attachment_path, "rb") as f:
        mime_app = MIMEApplication(
          f.read(),
          Name=attachment_path.name
        )
      mime_app['Content-Disposition'] = f'attachment; filename="{attachment_path.name}"'
      mime_multi_part.attach(mime_app)

    server = smtplib.SMTP(self.__email_smtp_server, self.__email_smtp_server_port)
    if self.__email_use_tls:
      server.starttls()
    if self.__email_auth_id:
      server.login(self.__email_auth_id, self.__email_auth_pw)
    server.send_message(mime_multi_part)
    server.quit()


  def send(self, subject: str, body: str, attachment_path: pathlib.Path=None):
    if self.__use_slack_webhook:
      self.__slack_webhook(subject,body)
    if self.__use_line:
      self.__line(subject,body)
    if self.__use_email:
      self.__email(subject,body,attachment_path)