# Backlog

## Iteration +1
- Release v0.0.0

## Iteration +2
- Report: `InvalidColumnNameException["_fivetran_synced" conflicts with system column pattern]`
- Documentation: Project
- Documentation: CrateDB Examples
- Documentation: CrateDB Guide
- Documentation: Upstream

## Iteration +3
- Mechanism to ignore errors
- Currently, the machinery does not discriminate between `truncate_before`
  vs. `soft_truncate_before` or `delete` vs. `soft_delete`
- Currently, the machinery does not invoke any `REFRESH TABLE` statements (caveat!)
- The machinery renames all `_fivetran*` columns to `__fivetran*`
- Import Parquet?

## Iteration +4
- Consider using Golang or Java, like others are doing it

## Done
- Make it work
- Add integration test harness
- Basic/easy connectivity using `SQLALCHEMY_CRATEDB_URL`,
  for connecting to CrateDB and CrateDB Cloud.
- Complete `DataType.*` and `RecordType.{UPSERT,UPDATE,DELETE,TRUNCATE}`,
  see `cratedb_fivetran_destination/sdk_pb2/common_pb2.pyi`.
