import requests


def load_dashboard():
    with open('Docker/kibana/dashboard/export.ndjson', 'r', encoding='utf-8') as f:
        data = f.read()

    headers = {'kbn-xsrf': 'true'}
    files = {'file': ('request.ndjson', data)}
    req = requests.post('http://elastic:changeme@localhost:5601/api/saved_objects/_import?overwrite=true',
                        files=files, headers=headers)
