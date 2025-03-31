# CrateDB Fivetran Destination Changelog

## Unreleased

## v0.0.1 - 2025-03-31
- Added implementation for `DescribeTable` gRPC method
- Added implementation for `AlterTable` gRPC method
- Type mapping: Mapped `Fivetran.SHORT` to `SQLAlchemy.SmallInteger`
- Type mapping: Mapped `SQLAlchemy.DateTime` to `Fivetran.UTC_DATETIME`
- UI: Removed unneeded form fields. Added unit test.
- CLI: Provided command-line interface for `--port` and `--max-workers` options
- OCI: Provided container image `ghcr.io/crate/cratedb-fivetran-destination`
- Packaging: Removed SDK from repository, build at build-time instead

## v0.0.0 - 2025-02-17
- Added project skeleton
- Added generated SDK gRPC API stubs
- Added example destination blueprint
- Added software integration tests
- DML: Added SQLAlchemy backend implementation for upsert, update, delete
- Connect: Added `url` form field, accepting an SQLAlchemy database connection URL
- Connect: Implemented adapter's `Test` method
- Transform: Fivetran uses special values for designating `NULL` and
  CDC-unmodified values.
- Types: Added support for all Fivetran data types
