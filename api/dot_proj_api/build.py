import base64
import io
import docker
from docker.errors import ContainerError
from flask import (
    Blueprint, request, send_file, redirect, flash
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


@bp.route('/', methods=["GET", "POST"])
def build():
    if request.method == 'POST':
        container = None
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        try:
            data = base64.b64encode(file.read()).decode('utf-8')
            status_code, container = run(data)
            stdout = container.logs().decode()
            container.remove()
            if status_code == 0:
                btsIO = io.BytesIO()
                btsIO.write(base64.b64decode(stdout))
                btsIO.seek(0)
                outfile = file.filename.split('.', 1)[0]+"-out.zip"
                return send_file(btsIO,
                                 attachment_filename=outfile,
                                 as_attachment=True)
            else:
                return stdout, 400
        except ContainerError as err:
            return (container.logs() if container else str(err)), 500

    return """<!doctype html>
    <title>Upload new Project</title>
    <h1>Upload new Project</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Process>
    </form>
    """
