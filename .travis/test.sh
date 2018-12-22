#!/bin/bash

echo "API..."
(cd api && coverage run -m pytest)

echo "BUILDER..."
(cd builder && coverage run -m pytest)
