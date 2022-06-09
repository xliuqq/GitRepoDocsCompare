#!/bin/bash


base_dir=$(cd `dirname $0`; pwd)

echo $base_dir

pid=$(ps -ef | grep run.py | grep -v grep | awk '{print $2}')

if [ $pid"x" == "x" ] ; then
   $base_dir/start.sh
fi




