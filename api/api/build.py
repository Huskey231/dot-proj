"""Flask API Endpoint for /build

"""

import base64
import io
import docker
from docker.errors import ContainerError
from flask import (
    Blueprint, request, send_file, redirect
)

CLIENT = docker.from_env()

BLUEPIRNT = Blueprint('build', __name__, url_prefix='/build')


def run(data):
    """runs the polyglot build container
    :param data: base64 string encoded zip build file
    :returns: the build container instance
    """
    container = CLIENT.containers.run("zenoscave/dot-proj-builder:latest",
                                      detach=True,
                                      environment=[f"DOT_PROJ_BUILD='{data}'"])
    container.wait()
    return container


@BLUEPIRNT.route('', methods=["GET", "POST"])
def build():
    """The /build route
    """
    if request.method == 'POST':
        container = None
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if not file.filename.endswith('.zip'):
            return redirect(request.url)
        try:
            data = base64.b64encode(file.read()).decode('utf-8')
            container = run(data)
            stdout = container.logs().decode()
            container.remove()

            bts_io = io.BytesIO()
            bts_io.write(base64.b64decode(stdout))
            bts_io.seek(0)
            outfile = file.filename.split('.', 1)[0]+"-out.zip"
            return send_file(bts_io,
                             attachment_filename=outfile,
                             as_attachment=True)
        except ContainerError as err:  # pragma no cover
            return (container.logs() if container else str(err)), 500

    return """<!doctype html>
    <title>Upload new Project</title>
    <h1>Upload new Project</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Process>
    </form>
    """
