#!/bin/bash
set -o pipefail
source $(pipenv --venv)/bin/activate
#while [ true ] ;do
    git pull
    cp Pipfile.lock Pipfile.lock.old
    pipenv lock
    cmp --silent Pipfile.lock.old Pipfile.lock || pipenv sync
    ./main.py
    echo $?
#done
