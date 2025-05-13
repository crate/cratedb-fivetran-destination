# Backlog

## Iteration +0
- Performance: https://github.com/crate/cratedb-fivetran-destination/issues/11
- Interoperability: https://github.com/crate/cratedb-fivetran-destination/issues/8

## Iteration +1
- Does `SELECT '100.23'::BIGINT;` work on PostgreSQL?
- Introduce parameter handling to type mappers,
  re. timestamp and decimal types
- AlterTable: Implement `AlterTableRecreateStatements`
- Soft deletes: Currently, the machinery does not discriminate between
  `truncate_before` vs. `soft_truncate_before` or `delete` vs. `soft_delete`
- General refactoring: `main.py` vs. `engine.py`
- General docs: Improve inline comments
- Submit report to https://github.com/crate/crate/issues/15161.
  `InvalidColumnNameException["_fivetran_synced" conflicts with system column pattern]`
  possibly from `test_processor_failing`?
- Check FIXME and TODO items in code
- Propagate `warning` messages into responses
- Release v0.0.1

## Iteration +2
- Error `ValueError: I/O operation on closed file.` when tearing down the test suite,
- Documentation: The machinery renames all `_fivetran*` columns to `__fivetran*`
- Documentation: Don't use `print` for debugging purposes
- Documentation: CrateDB Guide
- Documentation: Upstream

## Iteration +3
- Does the SQL code need to escape SQL identifiers?
- Mechanism to ignore errors?
- Currently, the machinery does not invoke any `REFRESH TABLE` statements (caveat!)
- Import Parquet for testing purposes?

## Iteration +4
- Consider using Golang or Java, like others are doing it
  https://github.com/crate/cratedb-fivetran-destination/issues/11

## Done
- Make it work
- Add integration test harness
- Basic/easy connectivity using `SQLALCHEMY_CRATEDB_URL`,
  for connecting to CrateDB and CrateDB Cloud.
- Complete `DataType.*` and `RecordType.{UPSERT,UPDATE,DELETE,TRUNCATE}`,
  see `cratedb_fivetran_destination/sdk_pb2/common_pb2.pyi`.
- Release v0.0.0
- Strip UI fields, just use `url`
