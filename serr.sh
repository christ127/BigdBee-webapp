#!/bin/bash

echo "serr $1 $2 $3"

task=$1
ltype=$2
jobid=$3

echo "task  = $task  (tags)"
echo "ltype  = $ltype  (err, out)"
echo "jobid = $jobid"

log=slurm-$jobid.$ltype.txt
if [[ "$task" == "tags" ]]; then
   log="/work/rmegret/rmegret/tags/apriltag-$jobid.$ltype.txt"
elif [[ "$task" == "avi2mpg" ]]; then
   log="/work/rmegret/rmegret/videos/avi2mpg-$jobid.$ltype.txt"
elif [[ "$task" == "merge" ]]; then
   log="/work/rmegret/rmegret/tags/mergetag-$jobid.$ltype.txt"
elif [[ "$task" == "clean" ]]; then
   log="/work/rmegret/rmegret/tags/cleantag-$jobid.$ltype.txt"
else
   echo "unknown task '$type'"
fi

echo "Trying $ltype log $log"
less $log
