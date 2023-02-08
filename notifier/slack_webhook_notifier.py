import json
import urllib

def notify(webhook_url: str, subject: str, body: str):
    params = {"text": f"{subject}\n{body}"}
    params_json = json.dumps(params)
    data = params_json.encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(webhook_url, data, headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        result = body.decode("utf-8")
        print(result)
