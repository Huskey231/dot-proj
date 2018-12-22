import os
import io

def good_data():
    with open(os.path.join(os.path.dirname(__file__), 'project.zip'), 'rb') as obj:
        return io.BytesIO(obj.read())


def test_build_success(client):
    response = client.post('/build/', data={'file': (good_data(), 'test.zip')},
                           follow_redirects=True,
                           content_type='multipart/form-data')
    assert response.status_code == 200

    response = client.get('/build', follow_redirects=True)
    assert response.status_code == 200
    assert b'Upload new Project' in response.data


def test_no_files(client):
    response = client.post('/build/', data={},
                           follow_redirects=True,
                           content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Upload new Project' in response.data

    response = client.post('/build/', data={'file': (good_data(), 'tgz')},
                           follow_redirects=True,
                           content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Upload new Project' in response.data
