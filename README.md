# CrateDB Fivetran Destination

[![Bluesky][badge-bluesky]][project-bluesky]
[![Release Notes][badge-release-notes]][project-release-notes]
[![CI][badge-ci]][project-ci]
[![Downloads per month][badge-downloads-per-month]][project-downloads]

[![Package version][badge-package-version]][project-pypi]
[![License][badge-license]][project-license]
[![Status][badge-status]][project-pypi]
[![Supported Python versions][badge-python-versions]][project-pypi]

» [Documentation]
| [Changelog]
| [PyPI]
| [Issues]
| [Source code]
| [License]
| [CrateDB]
| [Community Forum]

The `cratedb-fivetran-destination` package implements the [CrateDB destination
adapter for Fivetran]. It works with both [CrateDB] and [CrateDB Cloud].

Feel free to use the adapter as provided or else modify / extend it
as appropriate for your own applications. We appreciate contributions of any kind.

## Introduction

CrateDB is a distributed and scalable SQL database for storing and analyzing
massive amounts of data in near real-time, even with complex queries.
It is PostgreSQL-compatible, and based on Lucene.

Fivetran is an automated data movement platform. Automatically, reliably and
securely move data from 650+ sources including SaaS applications, databases,
ERPs, and files to data warehouses, data lakes, and more.

## Installation

```bash
pip install --upgrade cratedb-fivetran-destination
```

## Usage

Start gRPC destination server.
```bash
python -m cratedb_fivetran_destination.main
```

## Requirements

The package is based on [CrateDB's SQLAlchemy dialect] package.
It will be automatically installed when installing the Fivetran adapter.

You can run [CrateDB Self-Managed] or start using [CrateDB Cloud],
see [CrateDB Installation], or [CrateDB Cloud Console].

## Usage

To learn about the Fivetran destination adapter for CrateDB, please refer to the
documentation and examples:

- FIXME


## Project Information

### Acknowledgements
Kudos to the authors of all the many software components this library is
inheriting from and building upon.

### Contributing
The `cratedb-fivetran-destination` package is an open source project, and is
[managed on GitHub]. We appreciate contributions of any kind.

### License
The project uses the Apache license, like CrateDB itself.


[CrateDB]: https://cratedb.com/database
[CrateDB Cloud]: https://cratedb.com/database/cloud
[CrateDB Cloud Console]: https://console.cratedb.cloud/
[CrateDB Installation]: https://cratedb.com/docs/guide/install/
[CrateDB Self-Managed]: https://cratedb.com/database/self-managed
[CrateDB's SQLAlchemy dialect]: https://cratedb.com/docs/sqlalchemy-cratedb/
[CrateDBVectorStore]: https://github.com/crate-workbench/cratedb-fivetran-destination/blob/cratedb/docs/vectorstores.ipynb
[crate]: https://pypi.org/project/crate/

[Changelog]: https://github.com/crate-workbench/cratedb-fivetran-destination/blob/cratedb/CHANGES.md
[Community Forum]: https://community.cratedb.com/
[Documentation]: https://cratedb.com/docs/guide/integrate/fivetran/
[Issues]: https://github.com/crate-workbench/cratedb-fivetran-destination/issues
[License]: https://github.com/crate-workbench/cratedb-fivetran-destination/blob/cratedb/LICENSE
[managed on GitHub]: https://github.com/crate-workbench/cratedb-fivetran-destination
[PyPI]: https://pypi.org/project/cratedb-fivetran-destination/
[Source code]: https://github.com/crate-workbench/cratedb-fivetran-destination

[badge-bluesky]: https://img.shields.io/badge/Bluesky-0285FF?logo=bluesky&logoColor=fff&label=Follow%20%40CrateDB
[badge-ci]: https://github.com/crate-workbench/cratedb-fivetran-destination/actions/workflows/tests.yml/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/cratedb-fivetran-destination/month
[badge-license]: https://img.shields.io/github/license/crate-workbench/cratedb-fivetran-destination.svg
[badge-package-version]: https://img.shields.io/pypi/v/cratedb-fivetran-destination.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/cratedb-fivetran-destination.svg
[badge-release-notes]: https://img.shields.io/github/release/crate-workbench/cratedb-fivetran-destination?label=Release+Notes
[badge-status]: https://img.shields.io/pypi/status/cratedb-fivetran-destination.svg
[project-bluesky]: https://bsky.app/search?q=cratedb
[project-ci]: https://github.com/crate-workbench/cratedb-fivetran-destination/actions/workflows/tests.yml
[project-downloads]: https://pepy.tech/project/cratedb-fivetran-destination/
[project-license]: https://github.com/crate-workbench/cratedb-fivetran-destination/blob/cratedb/LICENSE
[project-pypi]: https://pypi.org/project/cratedb-fivetran-destination
[project-release-notes]: https://github.com/crate-workbench/cratedb-fivetran-destination/releases
