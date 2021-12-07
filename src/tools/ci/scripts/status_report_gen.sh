#!/bin/bash

# When a new job is added:
# 1.) add variable for job's name
# 2.) add variable for job artifact directory
# 3.) call get_status and populate description accordingly

#Job Names as defined in CI
docker_job="docker-job"
python_job="python-job"
react_native_job="react-native-job"
web_job="web-job"
smoke_test_job="smoke-test"
android_apk_publish_job="publish-android-apk"

#VARIABLES
success="success"
failure="failure"
description=""

ci_status_json=ci_status.json

#LIST OF DOWNLOAD ARTIFACT DIRECTORIES CREATED BY CI

    #The directory names(values below) are the names of the artifact.
    #The names are declared as environment variables for each job and 
    #are set as the artifact name in the jobs' upload step

docker_cms_dir="artifact-$docker_job-cms"
docker_keycloak_dir="artifact-$docker_job-keycloak"
docker_mibs_dir="artifact-$docker_job-mibs"
docker_postgres_dev_dir="artifact-$docker_job-postgres-dev"
docker_reverse_proxy_dir="artifact-$docker_job-reverse-proxy"
docker_smtp_dev_dir="artifact-$docker_job-smtp-dev"
docker_web_dir="artifact-$docker_job-web"
python_cms_dir="artifact-$python_job-cms"
python_mibs_dir="artifact-$python_job-mibs"
react_native_dir="artifact-$react_native_job"
web_dir="artifact-$web_job"
smoke_test_dir="artifact-$smoke_test_job"
android_apk_publish_dir="artifact-$android_apk_publish_job"

get_status(){
    if [ -d $1 ];
    then 
        if [ -n "$3" ];
        then
            value=$(jq ".\"$2\"" $1/$ci_status_json | jq ".\"$3\"")
        else
            value=$(jq ".\"$2\"" $1/$ci_status_json)
        fi

        echo "$value"
    else
        echo "unknown"
    fi
}

populate_description(){

    description+=$1
}

report(){
    status=$success
    # populate docker-cms job status
    stat="$(get_status $docker_cms_dir $docker_job 'cms')"
    populate_description "docker-cms[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-keycloak job status
    stat="$(get_status $docker_keycloak_dir $docker_job 'keycloak')"
    populate_description "docker-keycloak[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi
    
    # populate docker-mibs job status
    stat="$(get_status $docker_mibs_dir $docker_job 'mibs')"
    populate_description "docker-mibs[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-postgres-dev job status
    stat="$(get_status $docker_postgres_dev_dir $docker_job 'postgres-dev')"
    populate_description "docker-postgres-dev[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-reverse-proxy job status
    stat="$(get_status $docker_reverse_proxy_dir $docker_job 'reverse-proxy')"
    populate_description "docker-reverse-proxy[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-smtp-dev job status
    stat="$(get_status $docker_smtp_dev_dir $docker_job "smtp-dev")"
    populate_description "docker-smtp-dev[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-web job status
    stat="$(get_status $docker_web_dir $docker_job "web")"
    populate_description "docker-web[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate docker-mibs job status
    stat="$(get_status $docker_mibs_dir $docker_job "mibs")"
    populate_description "docker-mibs[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate python-cms job status
    stat="$(get_status $python_cms_dir $python_job "cms")"
    populate_description "python-cms[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate python-mibs job status
    stat="$(get_status $python_mibs_dir $python_job "mibs")"
    populate_description "python-mibs[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate react-native job status
    stat="$(get_status $react_native_dir $react_native_job)"
    populate_description "react-native[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate web job status
    stat="$(get_status $web_dir $web_job)"
    populate_description "web[$stat], \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate smoke test job status
    stat="$(get_status $smoke_test_dir $smoke_test_job)"
    populate_description "smoke-test[$stat] \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    # populate android apk build job status
    stat="$(get_status $android_apk_publish_dir $android_apk_publish_job)"
    populate_description "android-apk-publish[$stat] \n"
    if [ "$stat" = "$failure" ];then
        status=$failure
    fi

    description+="$status"
    echo $description
}

report