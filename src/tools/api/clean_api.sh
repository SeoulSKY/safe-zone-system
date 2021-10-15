#!/bin/bash -e

DIR_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../lib/mibs/ts" && pwd)"

cd $DIR_PATH
rm -rf openapi