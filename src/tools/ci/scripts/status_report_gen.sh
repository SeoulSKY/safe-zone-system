#!/bin/bash

#VARIABLES
docker_job="docker-job"
python_job="python-job"
react_native_job="react-native-job"
web_job="web-job"
smoke_test_job="smoke-test"

success="success"
failure="failure"
value=""

description=""
status=$success

ci_status_json=ci_status.json

#LIST OF DOWNLOAD ARTIFACT DIRECTORIES CREATED BY CI

    #The directory names(values below) are the names of the artifact.
    #The names are declared as environment variables for each job and 
    #are set as the artifact name the jobs' upload step

docker_cms_dir="artifact-docker-job-cms"
docker_keycloak_dir="artifact-docker-job-keycloak"
docker_mibs_dir="artifact-docker-job-mibs"
docker_postgres_dev_dir="artifact-docker-job-postgres-dev"
docker_reverse_proxy_dir="artifact-docker-job-reverse-proxy"
docker_smtp_dev_dir="artifact-docker-job-smtp-dev"
docker_web_dir="artifact-docker-job-web"
python_cms_dir="artifact-python-job-cms"
python_mibs_dir="artifact-python-job-mibs"
react_native_dir="artifact-react-native-job"
web_dir="artifact-web-job"
smoke_test_dir="artifact-smoke-test"

get_status(){
    if [ -d $1 ];
    then 
        if [ -n "$3" ];
        then
            value=$(jq ".\"$2\"" $1/$ci_status_json | jq ".\"$3\"")
        else
            value=$(jq ".\"$2\"" $1/$ci_status_json)
        fi

        if [ "$value" = "$failure" ];then
            status="$failure"
        fi
        
        echo $value
    else
        echo "unknown"
    fi
}

populate_description(){

    description+=$1
}

report(){

    # populate docker-cms job status
    stat="$(get_status $docker_cms_dir $docker_job 'cms')"
    populate_description "docker-cms[$stat], \n"

    # populate docker-keycloak job status
    stat="$(get_status $docker_keycloak_dir $docker_job 'keycloak')"
    populate_description "docker-keycloak[$stat], \n"

    # populate docker-mibs job status
    stat="$(get_status $docker_mibs_dir $docker_job 'mibs')"
    populate_description "docker-mibs[$stat], \n"

    # populate docker-postgres-dev job status
    stat="$(get_status $docker_postgres_dev_dir $docker_job 'postgres-dev')"
    populate_description "docker-postgres-dev[$stat], \n"

    # populate docker-reverse-proxy job status
    stat="$(get_status $docker_reverse_proxy_dir $docker_job 'reverse-proxy')"
    populate_description "docker-reverse-proxy[$stat], \n"

    # populate docker-smtp-dev job status
    stat="$(get_status $docker_smtp_dev_dir $docker_job "smtp-dev")"
    populate_description "docker-smtp-dev[$stat], \n"

    # populate docker-web job status
    stat="$(get_status $docker_web_dir $docker_job "web")"
    populate_description "docker-web[$stat], \n"

    # populate docker-mibs job status
    stat="$(get_status $docker_mibs_dir $docker_job "mibs")"
    populate_description "docker-mibs[$stat], \n"

    # populate python-cms job status
    stat="$(get_status $python_cms_dir $python_job "cms")"
    populate_description "python-cms[$stat], \n"

    # populate python-mibs job status
    stat="$(get_status $python_mibs_dir $python_job "mibs")"
    populate_description "python-mibs[$stat], \n"

    # populate react-native job status
    stat="$(get_status $react_native_dir $react_native_job)"
    populate_description "react-native[$stat], \n"

    # populate web job status
    stat="$(get_status $web_dir $web_job)"
    populate_description "web[$stat], \n"

    # populate smoke test job status
    stat="$(get_status $smoke_test_dir $smoke_test_job)"
    populate_description "smoke-test[$stat] \n"

    description+="$status"
    echo $description
}

report