import os
import shlex
import zipfile
import tempfile
import io
import base64
import glob
import sys
import json

from subprocess import Popen, PIPE

__all__ = ['make']


def make(data):
    source = tempfile.TemporaryDirectory()
    try:
        file_bytes = base64.b64decode(data)
        file = io.BytesIO(file_bytes)
        with source as temp_dir:
            with zipfile.ZipFile(file) as zip_ref:
                zip_ref.extractall(temp_dir)

            return make_build(temp_dir)
    except:
        return ""


def make_build(source_directory):
    build = tempfile.TemporaryDirectory()

    path = os.path.join(source_directory, '.proj.json')
    if not os.path.isfile(path):
        return ""

    with open(path) as file:
        request = json.load(file)

    with build as temp_dir:
        cmd = shlex.split(request['build']) + [temp_dir]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=source_directory)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            print(stdout.decode(), file=sys.stderr)
            print(stderr.decode(), file=sys.stderr)

        return make_dist(request, temp_dir)


def make_dist(request, build_directory):
    distribution = io.BytesIO()
    with zipfile.ZipFile(distribution, 'w') as zip_ref:
        for pattern in request['dist']:
            path_pattern = os.path.join(build_directory, pattern)
            for file in glob.glob(path_pattern):
                path = os.path.relpath(file, build_directory)
                zip_ref.write(file, arcname=path, compress_type=zipfile.ZIP_DEFLATED)

    dist_bytes = distribution.getvalue()
    return base64.b64encode(dist_bytes).decode('utf-8')
