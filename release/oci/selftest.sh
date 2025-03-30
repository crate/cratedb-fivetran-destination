#!/bin/bash

# Fail on error.
set -e

# Display all commands.
# set -x

echo "Invoking adapter"
cratedb-fivetran-destination --version
