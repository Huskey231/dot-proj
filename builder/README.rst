DotProj/Builder
===============

The Build engine for dotProj


Install
-------

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the master branch. ::

    # clone the repository
    git clone https://github.com/zenoscavesoftware/dot-proj
    cd dot-proj/builder
    # checkout the correct version
    git tag  # shows the tagged versions
    git checkout latest-tag-found-above

Create a virtualenv and activate it::

    python3 -m venv venv
    . venv/bin/activate

Or on Windows cmd::

    py -3 -m venv venv
    venv\Scripts\activate.bat

Install the Builder::

    pip install -e .

Run
---

::

    export DOT_PROJ_BUILD="$(base64 < path/file.zip)"
    dotproj-build

Or on Windows cmd::

    TODO: SHOW WINDOWS COMMANDS

Test
----

::

    pip install '.[test]'
    pytest

Run with coverage report::

    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser

