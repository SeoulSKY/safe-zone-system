
#!/bin/bash -e

DIR_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"

docker run --rm \
  -v "${DIR_PATH}":/local openapitools/openapi-generator-cli generate \
  -i /local/tools/api/openapi.yml \
  -g typescript-axios \
  -o /local/lib/mibs/ts/openapi

