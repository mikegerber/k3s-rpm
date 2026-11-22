#!/usr/bin/env -S just --justfile

default: build

build:
  spectool -g k3s.spec
  rpmbuild -ba k3s.spec --define "_sourcedir $(pwd)"
