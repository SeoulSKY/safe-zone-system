#!/bin/bash -e

DIR_PATH="$(cd "$(dirname "$0")/../../lib/mibs/ts" && pwd)"

cd $DIR_PATH
rm -rf openapi