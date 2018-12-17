#!/bin/bash

source="$(pwd)"
cd "$1" && cmake "${source}" && make
