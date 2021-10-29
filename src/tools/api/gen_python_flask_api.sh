#!/bin/sh -e

# gen_python_flask_api.sh
#
# Generate a Python-Flask module for a given API.
#
# Arguments:
#   - $1 an openapi document
#   - $2 the output directory of the API library
#
# Pre-conditions:
#   - node must be installed
#
# Post-conditions:
#   - creates the pf/openapi directories in the given output directory or
#       the default: /src/tools/api/openapi.yml
#   - generates a Python-Flask module in the directory $2/pf/openapi or the
#       default: /src/lib/mibs/pf
#
# Example:
# generate the mibs api module:
#   - `$ ./gen_api.sh openapi.yml ../../lib/mibs/pf`

DIR_PATH="$(dirname "$0")/../../"

java -jar swagger-codegen-cli.jar generate -l python-flask \
  -i "${1:-$DIR_PATH/tools/api/openapi.yml}" \
  -o "${2:-$DIR_PATH/lib/mibs/python}"/openapi
