#!/bin/bash

# build
find -name Dockerfile -exec bash -c "echo {} | cut -d / -f2- | rev | cut -d / -f2- | rev " \; | xargs -n1 -I{} docker build --rm --tag="zenoscave/dot-proj-$(echo {} | tr / -)":latest {}

# deploy
docker images "zenoscave\/*:latest" | cut -d ' ' -f1 | grep 'zenoscave' | xargs docker push