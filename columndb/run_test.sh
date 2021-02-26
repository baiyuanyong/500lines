#!/bin/bash

mkdir DATA

python -m unittest discover tests -v

rm -rf DATA