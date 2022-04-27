#!/bin/sh

cd docker
start_postgres=
start_smtp=
tag=
case $3 in
  p*)
    echo adding postgress
    start_postgres='-f ./local/docker-compose.postgres.yml'
    ;;
  s*)
    echo adding smtp
    start_smtp='-f ./local/docker-compose.smtp.yml'
    ;;
esac
case $4 in
  p*)
    echo adding postgress
    start_postgres='-f ./local/docker-compose.postgres.yml'
    ;;
  s*)
    echo adding smtp
    start_smtp='-f ./local/docker-compose.smtp.yml'
    ;;
esac
case $2 in
  t*)
    echo starting test
    cd test
    AUTH_ISSUER=$1 docker-compose --env-file ./local/local-test.env -f docker-compose.yml ${start_postgres} ${start_smtp} up
    ;;
  *)
    echo starting devsudo docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs sudo docker rm
    cd dev
    AUTH_ISSUER=$1 docker-compose --env-file ./dev.env up --build
    ;;
esac
