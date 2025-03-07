# Development Documentation

## Set up sandbox
```shell
git clone https://github.com/crate/cratedb-fivetran-destination.git
cd cratedb-fivetran-destination
uv venv --seed
source .venv/bin/activate
uv pip install --upgrade --editable='.[develop,test]'
```

## Validate codebase
Run linters and software tests.
```shell
poe check
```
Format code.
```shell
poe format
```

## Software tests

### Unit tests

Run tests selectively.
```shell
pytest -vvv tests/test_foo.py tests/test_examples.py
```
```shell
pytest -vvv -k standard
```
```shell
pytest -vvv -k cratedb
```

### Integration tests

Start CrateDB.
```shell
docker run --rm \
  --publish=4200:4200 --publish=5432:5432 --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
```

Start gRPC destination server.
```bash
python -m cratedb_fivetran_destination.main
```

[Install the gcloud CLI] and start [Fivetran destination tester].
```shell
gcloud auth configure-docker us-docker.pkg.dev
```
```shell
docker run --rm -it \
  --mount type=bind,source=$(pwd)/tests/data,target=/data \
  -a STDIN -a STDOUT -a STDERR \
  -e WORKING_DIR=$(pwd)/tests/data \
  -e GRPC_HOSTNAME=host.docker.internal \
  --network=host \
  us-docker.pkg.dev/build-286712/public-docker-us/sdktesters-v2/sdk-tester:2.25.0131.001 \
  --tester-type destination --port 50052
```


## Release
```shell
poe release
```


[Fivetran destination tester]: https://github.com/fivetran/fivetran_sdk/tree/v2/tools/destination-connector-tester
[Install the gcloud CLI]: https://cloud.google.com/sdk/docs/install
