import os
import shlex
import tarfile
import tempfile
import io
import base64
import glob
import sys
import json

from subprocess import Popen, PIPE


def make(data):
    source = tempfile.TemporaryDirectory()
    file_bytes = base64.b64decode(data)
    file = io.BytesIO(file_bytes)
    with source as temp_dir:
        with tarfile.open(fileobj=file, mode='r:*') as tar:
            members = tar.getmembers()
            tar.extractall(temp_dir, members)

        return make_build(temp_dir)


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
    with tarfile.open(fileobj=distribution, mode="w:gz") as tar:
        for pattern in request['dist']:
            path_pattern = os.path.join(build_directory, pattern)
            for file in glob.glob(path_pattern):
                path = os.path.relpath(file, build_directory)
                with open(file, 'rb') as fd:
                    info = tarfile.TarInfo(path)
                    fd.seek(0, io.SEEK_END)
                    info.size = fd.tell()
                    fd.seek(0, io.SEEK_SET)
                    tar.addfile(info, fd)

    dist_bytes = distribution.getvalue()
    return base64.b64encode(dist_bytes).decode('utf-8')


if __name__ == '__main__':
    env = os.environ.get('DOT_PROJ_BUILD', '')
    try:
        print(make(env))
    except:
        print(env)
