#!/bin/bash

time="${1-6 hours ago}"
user="${2-$(whoami)}"

d="$(date -d "$time" '+%Y-%m-%dT%H:%M:%S')"

echo "sjobs: Jobs for user $user for period '$time'"
echo "starttime after $d"

sacct -u rmegret --starttime "$d" -n -o jobid%18,jobidraw%12,jobname%36,state%20,start,elapsed,timelimit | grep -v '[0-9][.]batch' | awk 'BEGIN{a=""} {vid=$3; sub("tags-","",vid); sub("-0-72100","",vid); if ($3!=a) print vid; a=$3; print}'

exit 0

J=$(sacct -u rmegret --starttime "$d" -n -o jobid%20,jobidraw%20,jobname%30 \
    | grep -v '[0-9][.]batch' | awk '{split($1,arr,"_"); gsub(/\[/,"",arr[1]); gsub(/\]/,"",arr[1]); printf("%s,%s,%s,%s,%s\n",$1,$2,$3,arr[1],arr[2]);} '| sort -t , -k 3,3 -k 4,4n -k 5,5n)

#echo jobs: "$J"

Jarr="$(echo "$J" | awk -F , '{if ($2=="") next;   print $2","$3}')"

echo Jarr="$Jarr"

if [[ -z "$Jarr" || $Jarr == "," ]]; then
    echo "No jobs found"
    exit 0
fi

template=' %-13s  %8s  %-32s %10s %20s %9s %9s\n'
printf "$template" JOBID JOBIDRAW JOBNAME STATE START ELAPSED TIMELIMIT
lastid='000000'
lastname='___'
result=$(
for jx in $Jarr; do
   #echo $jx
   j="${jx%,*}"
   name="${jx#*,}"
   jd=$j 
   id=${j%_*}
   suffix=${j##*_}
   #if [ ${suffix:0:1} == "[" ]; then jd=id; fi
   #echo "### $j"
   #echo $lastname $name
   #if [ x"$lastname" !=  x"$name" ]; then echo ""; fi
   sacct -j $jd -p -n --format=jobid%10,jobidraw,jobname,state,start,elapsed,timelimit  \
   | grep -v "$jd\..*" \
   | awk -F '|' '{ \
       if ( $3 == "batch" ) { next; }; \
       split($4,arr," "); status=arr[1]; \
       printf("'"${template}"'", $1,$2,$3,status,$5,$6,$7,$8);\
     }' ; 
   lastid=$id
   lastname="$name"
done
)




echo "$result" | sort -k 3,3 -k 2,2 | sort -u -t _ -k 1,1n -k 2,2n | \
     uniq -w 30 | \
     awk 'BEGIN{lastname="";} {name=$3; if ( name != lastname ) print ""; print; lastname=name;}'
