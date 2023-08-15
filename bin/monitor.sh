#!/bin/bash

# monitor the timer process running status, if process not exist, start it.

base_dir=$(cd `dirname $0`; pwd)

echo $base_dir

pid=$(ps -ef | grep run.py | grep -v grep | awk '{print $2}')

if [ $pid"x" == "x" ] ; then
   $base_dir/start_timer_compare.sh
fi




