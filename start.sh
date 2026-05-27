#!/usr/bin/env bash
set -e
mkdir -p workspace/projects workspace/datasets workspace/exports workspace/.history
python backend/app.py
