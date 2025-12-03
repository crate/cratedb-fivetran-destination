# Development Documentation

## Introduction

For hacking on the destination connector, please familiarize yourself
with the [Fivetran SDK Development Guide].

## Set up sandbox
```shell
git clone https://github.com/crate/cratedb-fivetran-destination.git
cd cratedb-fivetran-destination
uv venv --python 3.13 --seed .venv
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

:::{note}
Use `gcloud auth login` to authenticate the Google SDK so you can pull the OCI images.
```shell
$ docker pull us-docker.pkg.dev/build-286712/public-docker-us/sdktesters-v2/sdk-tester:2.25.0131.001
error getting credentials - err: exit status 1, out: `You do not currently have an active account selected. See https://cloud.google.com/sdk/docs/authorizing for more information.`
```
:::

## Software tests

### Unit tests

Run tests selectively.
```shell
pytest tests/test_foo.py tests/test_examples.py
```
```shell
pytest -k standard
```
```shell
pytest -k cratedb
```
```shell
pytest -k "fivetran and ddl"
```

### Integration tests

Start CrateDB.
```shell
docker run --rm \
  --publish=4200:4200 --publish=5432:5432 --env=CRATE_HEAP_SIZE=2g \
  crate:latest '-Cdiscovery.type=single-node'
```

Start gRPC destination server.
```bash
cratedb-fivetran-destination
```

[Install the gcloud CLI], authenticate, and start the [Fivetran destination tester].
```shell
gcloud auth configure-docker us-docker.pkg.dev
```
```shell
fivetran-sdk-tester --directory=./tests/data/fivetran_canonical
```

## Building

### Dependencies
Write runtime dependencies to `requirements.txt` file.
```shell
uv run poe build-requirements
```

### Standalone builds
Build a standalone executable using PyInstaller.
```shell
uv pip install --upgrade --editable='.[release]'
uv run poe build-app
```

### OCI builds
Build OCI images on your workstation.
```shell
export BUILDKIT_PROGRESS=plain
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
```
```shell
docker build --tag=local/cratedb-fivetran-destination --file=release/oci/Dockerfile .
```
Roughly verify that invocation works.
```shell
docker run --rm local/cratedb-fivetran-destination --version
```

## Python package release

```shell
poe release
```


[Fivetran destination tester]: https://github.com/fivetran/fivetran_sdk/tree/v2/tools/destination-connector-tester
[Fivetran SDK Development Guide]: https://github.com/fivetran/fivetran_sdk/blob/main/development-guide.md
[Install the gcloud CLI]: https://cloud.google.com/sdk/docs/install
