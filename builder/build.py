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


def make_source(sreq):
    tmp_src = tempfile.mkdtemp()
    data = sreq['data'].encode('utf-8')
    file = io.BytesIO(base64.b64decode(data))
    with tarfile.open(fileobj=file, mode='r:*') as tar:
        tar.extractall(tmp_src, tar.getmembers())

    return tmp_src


def make_build(breq, src):
    tmp_bld = tempfile.mkdtemp()
    cmd = shlex.split(breq['build']+" "+tmp_bld)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=src)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        print(stdout.decode(), file=sys.stderr)
        print(stderr.decode(), file=sys.stderr)
    return tmp_bld


def make_dist(dreq, bld):
    tmp_dist = tempfile.mktemp()
    dist_patterns = dreq['dist']
    files = [file for pattern in dist_patterns for file in glob.glob(os.path.join(bld, pattern))]
    with tarfile.open(tmp_dist, mode="w|gz") as tar:
        for file in files:
            path = os.path.relpath(file, bld)
            with open(file, 'rb') as fd:
                info = tarfile.TarInfo(path)
                fd.seek(0, io.SEEK_END)
                info.size = fd.tell()
                fd.seek(0, io.SEEK_SET)
                tar.addfile(info, fd)

    return tmp_dist


if __name__ == '__main__':
    projects = {}

    for proj in sys.argv[1:]:
        with open(proj) as f:
            req = json.load(f)
        projects[proj] = make_dist(req, make_build(req, make_source(req)))

    print(json.dumps(projects))
