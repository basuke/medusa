#!/bin/bash
# venv の設定

python -mvenv ./venv/
. ./venv/bin/activate
pip install -r requirements.txt
