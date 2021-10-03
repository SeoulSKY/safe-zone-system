#!/bin/bash -e
docker run -d --rm -p 3000:8080 swaggerapi/swagger-editor
echo "Running swagger-editor at http://localhost:3000/"
