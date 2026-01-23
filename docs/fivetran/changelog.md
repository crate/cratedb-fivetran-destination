---
name: Release Notes
title: CrateDB Release Notes
description: Changelog for CrateDB Fivetran Destination
hidden: false
---

# Release Notes

## January 2026

Feature release.

- Feature: Improved `AlterTable` operations
- Feature: Added support for schema migrations
- Feature: Added support for history and live mode
- Types: Added support for Fivetran's `TIME_NAIVE` data type
- Compatibility: Field `_fivetran_deleted` became optional

## May 2025

Maintenance release.

## March 2025

Initial release.

- Added implementation for `DescribeTable` gRPC method
- Added implementation for `AlterTable` gRPC method
- Type mapping: Mapped `Fivetran.SHORT` to `SQLAlchemy.SmallInteger`
- Type mapping: Mapped `SQLAlchemy.DateTime` to `Fivetran.UTC_DATETIME`
- UI: Removed unneeded form fields. Added unit test.
- CLI: Provided command-line interface for `--port` and `--max-workers` options
- OCI: Provided container image `ghcr.io/crate/cratedb-fivetran-destination`
- Packaging: Removed SDK from repository, build at build-time instead
