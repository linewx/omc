#!/usr/bin/env bash

#build
python setup.py sdist bdist_wheel

#rm -fr dist/*
#upload
twine upload --repository pypi dist/*