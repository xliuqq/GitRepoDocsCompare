#!/bin/bash

base_dir=$(cd `dirname $0`; pwd)

cd $base_dir/../

nohup python3 run.py > logs/timer.log 2>&1 &
