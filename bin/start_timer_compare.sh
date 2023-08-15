#!/bin/bash

base_dir=$(cd `dirname $0`; pwd)

cd $base_dir/../

nohup python3 run.py > /dev/null 2>&1 &
