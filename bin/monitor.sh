#!/bin/bash

# monitor the timer process running status, if process not exist, start it.

base_dir=$(cd `dirname $0`; pwd)

pid=$(ps -ef | grep run.py | grep -v grep | awk '{print $2}')

if [ $pid"x" == "x" ] ; then
    echo "run process not found" 
    conda activate git_docs_compare
    $base_dir/start_timer_compare.sh
fi




