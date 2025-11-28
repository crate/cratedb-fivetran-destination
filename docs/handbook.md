# CrateDB destination adapter for Fivetran handbook

## Introduction

The package is based on [CrateDB's SQLAlchemy dialect] package, in turn using
the [crate] Python driver. Both packages will be automatically installed when
installing the Fivetran adapter.

You can run [CrateDB Self-Managed] or start using [CrateDB Cloud],
see [CrateDB Installation], or [CrateDB Cloud Console].

The project provides installation artefacts per [PyPI package][PyPI] and
[OCI image], you can invoke the adapter by installing it persistently
first, or by running it ephemerally using its container image.

## Persistent installation

Install package. [^uv]
```bash
uv tool install --upgrade cratedb-fivetran-destination
```

Start gRPC destination server. Note the parameters are optional.
```bash
cratedb-fivetran-destination --port=50052 --max-workers=1
```

## Standalone executables

CI on this project created standalone executables for different architectures
using [PyInstaller], and publishes them on its [releases] page.

## Container use

Invoke the OCI image [ghcr.io/crate/cratedb-fivetran-destination] at your
disposal, for example using Docker.
```bash
docker run --rm \
  --publish=50052:50052 \
  ghcr.io/crate/cratedb-fivetran-destination:nightly
```

CI is building image variants for each pr, each night, and for
GA releases, covering in many situations of the development cycle.

Please use container image tags appropriately when aiming for version pinning.
The first GA release will be `cratedb-fivetran-destination:0.0.1`.

## Caveats

:AlterTableRecreateStatements:

  When the adapter processes schema changes that involve amendments to primary
  keys, it needs to re-create the destination table and copy over all the
  data on behalf of a temporary table that will get swapped in after being
  populated. While the copy operation is taking place, the original table
  will block any writes, to avoid data loss.
  However, shortly before the table swap, to complete the operation, the
  adapter needs to release the write block: At this point,
  before completing the swap operation, CrateDB may accept writes to
  the original table before swapping it out, which may lead to data loss.
  To avoid any data loss, one should stop any writes during this operation.


[^uv]: We recommend to use the [uv] package manager, but it also works without.

[crate]: https://pypi.org/project/crate/
[CrateDB Cloud]: https://cratedb.com/database/cloud
[CrateDB Cloud Console]: https://console.cratedb.cloud/
[CrateDB Installation]: https://cratedb.com/docs/guide/install/
[CrateDB Self-Managed]: https://cratedb.com/database/self-managed
[CrateDB's SQLAlchemy dialect]: https://cratedb.com/docs/sqlalchemy-cratedb/
[ghcr.io/crate/cratedb-fivetran-destination]: https://github.com/crate/cratedb-fivetran-destination/pkgs/container/cratedb-fivetran-destination
[uv]: https://docs.astral.sh/uv/
[OCI image]: https://github.com/crate/cratedb-fivetran-destination/pkgs/container/cratedb-fivetran-destination
[PyInstaller]: https://pyinstaller.org/
[PyPI]: https://pypi.org/project/cratedb-fivetran-destination/
[releases]: https://github.com/crate/cratedb-fivetran-destination/releases
