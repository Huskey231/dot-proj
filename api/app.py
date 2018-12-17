import docker
import tempfile
import json
import base64
import sys
import os
from docker.errors import ContainerError
from flask import Flask, jsonify, request

app = Flask(__name__)
client = docker.from_env()
api = docker.APIClient()


def run(file):
    print(file, os.path.isfile(file))

    host_config = api.create_host_config(
        binds=["/tmp:/tmp"]
    )

    container = api.create_container(
        image="zenoscave/dot-proj-builder:latest",
        volumes=["/tmp"],
        host_config=host_config,
        user="1001:1001",
        command=[file]
    )
    api.start(container=container.get('Id'))
    return client.containers.get(container.get('Id'))


@app.route('/')
def index():
    return jsonify({}), 200


@app.route('/build', methods=["POST"])
def build():
    print(request.json)
    container = None
    try:
        tmp = tempfile.mktemp()
        with open(tmp, 'w') as file:
            json.dump(request.json, file)
        container = run(tmp)
        status_code = container.wait()['StatusCode']
        if status_code == 0:
            stdout = container.logs().decode()
            print(stdout)
            container.remove()
            data = json.loads(stdout)[tmp]
            with open(data, 'rb') as file:
                response = base64.b64encode(file.read())

            return jsonify({'response': response.decode()}), 200
        else:
            print(container.logs().decode(), '!!!!', file=sys.stderr)
            return '{}', 400

    except ContainerError as err:
        print(container, err)
        return jsonify({"error": container.logs() if container else str(err)}), 500

