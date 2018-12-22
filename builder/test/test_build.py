def test_build_not_base64(builder):
    assert builder.build.make("BAD_INFO") == ""


def test_build_not_zip(builder):
    import base64
    assert builder.build.make(base64.b64encode(b"BAD_INFO")) == ""


def test_missing_project_json(builder):
    import os
    import base64
    with open(os.path.join(os.path.dirname(__file__), 'no-proj.zip'), 'rb') as zip:
        output = builder.build.make(base64.b64encode(zip.read()))

    assert output == ""


def test_bad_build_command(capsys, builder):
    import os
    import base64

    with open(os.path.join(os.path.dirname(__file__), 'bad-command.zip'), 'rb') as zip:
        output = builder.build.make(base64.b64encode(zip.read()))
        captured = capsys.readouterr()

    assert captured.err != ""
    assert output == ""


def test_proper_project(builder):
    import os
    import base64
    with open(os.path.join(os.path.dirname(__file__), 'project.zip'), 'rb') as zip:
        output = builder.build.make(base64.b64encode(zip.read()))

    assert output != ""
    assert base64.b64decode(output) != ""
