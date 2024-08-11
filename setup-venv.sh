#!/bin/bash
# venv の設定

python -mvenv ./venv/
. ./venv/scripts/activate
pip install -r requirements.txt
