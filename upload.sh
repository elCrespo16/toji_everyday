#!/bin/bash

set -e

source /home/felipe/.bashrc


cd /home/felipe/toji_everyday
pyenv activate toji_everyday
pyenv exec python main.py >> toji_logs.log