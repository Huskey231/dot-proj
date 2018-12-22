#!/bin/bash

echo "API..."
(cd api && pip3 install -e '.[test]')

echo "BUILDER..."
(cd builder && pip3 install -e '.[test]')
