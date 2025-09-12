import requests

def send_request(method, url, headers=None, body=None):
    headers = headers or {}
    response = requests.request(method, url, headers=headers, json=body)
    return response