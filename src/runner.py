import json
import csv
import re
from src.utils.http_client import send_request

def run_request(method, url, headers_raw, body_raw):
    headers = json.loads(headers_raw) if headers_raw else {}
    body = json.loads(body_raw) if body_raw else None
    return send_request(method, url, headers, body)

def load_template(path):
    with open(path) as f:
        return f.read()

def load_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

def substitute_variables(template_str, variables):
    def replacer(match):
        key = match.group(1)
        return variables.get(key, match.group(0))
    return re.sub(r"\{\{(\w+)\}\}", replacer, template_str)

def run_batch_requests(method, url, headers_raw, body_template_str, csv_path):
    import csv, re
    headers = json.loads(headers_raw) if headers_raw else {}

    def substitute_variables(template, variables):
        def replacer(match):
            key = match.group(1)
            return variables.get(key, match.group(0))
        return re.sub(r"\{\{(\w+)\}\}", replacer, template)

    with open(csv_path, newline='') as f:
        rows = list(csv.DictReader(f))

    results = []
    for i, row in enumerate(rows, start=1):
        body_str = substitute_variables(body_template_str, row)
        body = json.loads(body_str)
        response = send_request(method, url, headers, body)

        try:
            parsed = response.json()
            pretty = json.dumps(parsed, indent=2)
        except Exception:
            pretty = response.text

        result = f"Status: {response.status_code}\n{pretty}"
        results.append(result)

    return results