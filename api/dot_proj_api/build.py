import json

import docker
from docker.errors import ContainerError
from flask import (
    Blueprint, request, jsonify
)

client = docker.from_env()
api = docker.APIClient()

bp = Blueprint('build', __name__, url_prefix='/build')


def run(data):
    container = client.containers.run("zenoscave/dot-proj-builder:latest",
                                      detach=True,
                                      environment=[f"DOT_PROJ_BUILD='{data}'"])
    status_code = container.wait()['StatusCode']
    return status_code, container


@bp.route('/', methods=["POST"])
def build():
    container = None
    req = request.json
    resp = {'projects': {}}
    for project, data in req.get('projects', {}).items():
        try:
            status_code, container = run(data)
            stdout = container.logs().decode()
            container.remove()
            if status_code == 0:
                resp['projects'][project] = {'success': stdout}
            else:
                resp['projects'][project] = {'error': stdout}
        except ContainerError as err:
            return jsonify({"error": container.logs() if container else str(err)}), 500

    return jsonify(resp), 200
