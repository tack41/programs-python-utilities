import urllib

def notify(token: str, subject: str, body: str):
    method = "POST"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {"message": f"{subject}\n{body}"}
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url="https://notify-api.line.me/api/notify", data=payload, method=method, headers=headers)
    urllib.request.urlopen(req)
