# Backlog

## Iteration +0
- Does the code need to escape SQL identifiers?
- Introduce parameter handling to type mappers
- Error `ValueError: I/O operation on closed file.` when tearing down the test suite,
  possibly from `test_processor_failing`?
- Check FIXME and TODO items in code.

## Iteration +1
- Propagate `warning` messages into responses
- Strip UI fields, just use `url`
- Scan for TODO and FIXME items
- Release v0.0.1

## Iteration +2
- Documentation: The machinery renames all `_fivetran*` columns to `__fivetran*`
- Currently, the machinery does not discriminate between `truncate_before`
  vs. `soft_truncate_before` or `delete` vs. `soft_delete`
- Documentation: CrateDB Guide
- Documentation: Upstream

## Iteration +3
- Submit report to https://github.com/crate/crate/issues/15161.
  `InvalidColumnNameException["_fivetran_synced" conflicts with system column pattern]`
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
