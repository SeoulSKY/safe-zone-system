#!/bin/sh -e

# gen_api.sh
#
# Generate a Typescript module for a given API.
#
# Arguments:
#   - $1 an openapi document
#   - $2 the output directory of the API library
#
# Pre-conditions:
#   - node must be installed
#
# Post-conditions:
#   - creates the ts/openapi directories in the given output directory or
#       the default: /src/tools/api/openapi.yml
#   - generates a Typescript module in the directory $2/ts/openapi or the
#       default: /src/lib/mibs/ts
#
# Example:
# generate the mibs api module:
#   - `$ ./gen_api.sh openapi.yml ../../lib/mibs/ts`

DIR_PATH="$(dirname "$0")/../../"

npx @openapitools/openapi-generator-cli generate -g typescript-axios \
  -i "${1:-$DIR_PATH/tools/api/openapi.yml}" \
  -o "${2:-$DIR_PATH/lib/mibs/ts}"/openapi

