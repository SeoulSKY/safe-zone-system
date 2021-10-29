#!/bin/bash

job_name=$1
job_status=$2
parent_name=$3
result=""
ci_status_json=$(dirname ci_status.json)/ci_status.json
echo $ci_status_json

if [ -n "$job_name" ] && [ -n "$job_status" ];
then
    if [ -n "$parent_name" ];
    then
        result=$(jq ".\"$parent_name\" += {\"$job_name\": \"$job_status\"}" $ci_status_json)
        echo $result 
        echo $result > $ci_status_json
    else
        result=$(jq ". += {\"$job_name\": \"$job_status\"}" $ci_status_json)
        echo $result
        echo $result > $ci_status_json
    fi
else
    echo "argument error"
    echo 0 #fail
fi
