#!/usr/bin/env bash
FILEPAHT=$1
PYTHON=~/Applications/miniconda3/envs/python3.7/bin/python
SCRIPT_PATH=~/Work/Coding/Owner/blog-auto-sender
SCRIPT=main.py

cd $SCRIPT_PATH && $PYTHON $SCRIPT $FILEPAHT