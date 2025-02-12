#!/bin/bash

# Make a directory protos
mkdir -p protos
cd protos
wget --no-clobber https://github.com/fivetran/fivetran_sdk/raw/refs/heads/main/common.proto
wget --no-clobber https://github.com/fivetran/fivetran_sdk/raw/refs/heads/main/connector_sdk.proto
wget --no-clobber https://github.com/fivetran/fivetran_sdk/raw/refs/heads/main/destination_sdk.proto
cd -

# Generate grpc python code and store it in sdk_pb2
outdir=cratedb_fivetran_destination/sdk_pb2
mkdir -p ${outdir}
python -m grpc_tools.protoc \
       --proto_path=./protos/ \
       --python_out=${outdir} \
       --pyi_out=${outdir} \
       --grpc_python_out=${outdir} protos/*.proto
