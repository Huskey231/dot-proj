import os
import json

with open(os.path.join(os.path.dirname(__file__), 'test.json')) as obj:
    good_data = obj.read()


def test_build(client, app):
    print(good_data)

    response = client.post('/build/', data='{}',
                           content_type='application/json')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == '{}'

    response = client.post('/build/', data=good_data,
                           content_type='application/json')
    assert response.status_code == 200
    respjson = json.loads(response.data.decode('utf-8'))
    assert 'response' in respjson
    assert respjson['response'] != ''
