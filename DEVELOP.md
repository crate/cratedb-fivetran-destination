# Development Documentation

## Set up sandbox
```shell
git clone https://github.com/crate-workbench/cratedb-fivetran-destination.git
cd cratedb-fivetran-destination
uv venv --seed
uv pip install --upgrade --editable='.[develop,test]'
```

## Run CrateDB
```shell
docker run --rm \
  --publish=4200:4200 --publish=5432:5432 --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
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

## Release
```shell
poe release
```
