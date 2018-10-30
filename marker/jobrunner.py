import json
import http.client
from urllib.error import HTTPError
from mako.template import Template

from marker.code_templates import CODE_TEMPLATES

# JOBE_SERVER = 'localhost:4000'
JOBE_SERVER = 'jobe2.cosc.canterbury.ac.nz'
USE_API_KEY = True
API_KEY = '2AAA7A5415B4A9B394B54BF1D2E9D'


def http_request(marking_server, method, resource, data, headers):
    if USE_API_KEY:
        headers['X-API-KEY'] = API_KEY
    connect = http.client.HTTPConnection(marking_server)
    connect.request(method, resource, data, headers)
    return connect


def do_http(marking_server, method, resource, data=None):
    result = {}
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    try:
        connect = http_request(marking_server, method, resource, data, headers)
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


def run_job(language, code, marking_server):
    run_spec = {
        'language_id': language,
        'sourcecode': code,
    }
    return do_http(
        marking_server,
        'POST',
        '/jobe/index.php/restapi/runs/',
        json.dumps({'run_spec': run_spec})
    )


def get_result(language, solution, test_case, code_template=None, helper_code='', marking_server=JOBE_SERVER):
    if not code_template:
        code_template = CODE_TEMPLATES[language]
    return run_job(
        language,
        Template(code_template).render(
            SOLUTION=solution,
            TEST_CASE=test_case,
            HELPER_CODE=helper_code
        ),
        marking_server
    )
