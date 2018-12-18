import os
import json

with open(os.path.join(os.path.dirname(__file__), 'test.json')) as obj:
    good_data = obj.read()


def test_build_empty(client, app):
    response = client.post('/build/', data='{}',
                           content_type='application/json')
    assert response.status_code == 200
    assert 'projects' in response.data.decode('utf-8')


def test_build_success(client, app):
    response = client.post('/build/', data=good_data,
                           content_type='application/json')
    assert response.status_code == 200
    respjson = json.loads(response.data.decode('utf-8'))
    assert 'projects' in respjson
    for project, dct in respjson['projects'].items():
        assert 'error' not in dct
