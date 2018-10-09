import json
import http.client
from urllib.error import HTTPError
from mako.template import Template


# JOBE_SERVER = 'localhost:4000'
JOBE_SERVER = 'jobe2.cosc.canterbury.ac.nz'
API_KEY = '2AAA7A5415B4A9B394B54BF1D2E9D'  # A working (100/hr) key on Jobe2
USE_API_KEY = True


def http_request(method, resource, data, headers):
    if USE_API_KEY:
        headers["X-API-KEY"] = API_KEY
    connect = http.client.HTTPConnection(JOBE_SERVER)
    connect.request(method, resource, data, headers)
    return connect


def do_http(method, resource, data=None):
    result = {}
    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    try:
        connect = http_request(method, resource, data, headers)
        response = connect.getresponse()
        if response.status != 204:
            content = response.read().decode('utf8')
            if content:
                result = json.loads(content)
        connect.close()
    except (HTTPError, ValueError) as e:
        if response:
            print(' Response:', response.status, response.reason, content)
        else:
            print(e)
    return result


def run_job(language, code, filename):
    runspec = {
        'language_id': language,
        'sourcefilename': filename,
        'sourcecode': code,
    }
    return do_http(
        'POST',
        '/jobe/index.php/restapi/runs/',
        json.dumps({'run_spec': runspec})
    )


def get_result(job_template, solution, test_case):
    result_obj = run_job(
        'python3',
        Template(job_template).render(SOLUTION=solution, TEST_CASE=test_case),
        'test.py'
    )
    try:
        return json.loads(result_obj['stdout'])
    except Exception:
        return None