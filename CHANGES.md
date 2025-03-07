# CrateDB Fivetran Destination Changelog


## Unreleased

## v0.0.0 - 2025-02-xx
- Added project skeleton
- Added generated SDK GRPC API stubs
- Added example destination blueprint
- Added software integration tests
- DML: Added SQLAlchemy backend implementation for upsert, update, delete
- Connect: Added `url` form field, accepting an SQLAlchemy database connection URL
- Connect: Implemented adapter's `Test` method
- Transform: Fivetran uses special values for designating `NULL` and
  CDC-unmodified values.
