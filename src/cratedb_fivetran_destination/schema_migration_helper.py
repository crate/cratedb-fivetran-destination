# ruff: noqa: E501,S608
# https://github.com/fivetran/fivetran_partner_sdk/blob/main/examples/destination_connector/python/schema_migration_helper.py
import typing as t
from copy import deepcopy

import sqlalchemy as sa

from cratedb_fivetran_destination.model import FieldMap, SqlBag, TypeMap
from cratedb_fivetran_destination.util import LOG_INFO, LOG_WARNING, log_message
from fivetran_sdk import common_pb2, destination_sdk_pb2

# Constants for system columns
FIVETRAN_START = "__fivetran_start"
FIVETRAN_END = "__fivetran_end"
FIVETRAN_ACTIVE = "__fivetran_active"


class SchemaMigrationHelper:
    """Helper class for handling migration operations"""

    def __init__(self, engine: sa.Engine, table_map):
        self.engine = engine
        self.table_map = table_map

    def handle_drop(self, drop_op, schema, table, table_obj):
        """
        Handles drop operations (drop table, drop column in history mode).

        - https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#drop_table
        - https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#drop_column_in_history_mode
        """
        entity_case = drop_op.WhichOneof("entity")

        if entity_case == "drop_table":
            sql = f'DROP TABLE "{schema}"."{table}"'
            with self.engine.connect() as conn:
                conn.execute(sa.text(sql))

            log_message(LOG_INFO, f"[Migrate:Drop] Dropping table {schema}.{table}")
            return destination_sdk_pb2.MigrateResponse(success=True)

        if entity_case == "drop_column_in_history_mode":
            drop_column = drop_op.drop_column_in_history_mode

            column_name = drop_column.column
            operation_timestamp = drop_column.operation_timestamp

            # Validate table is non-empty and `max(_fivetran_start) < operation_timestamp`.
            try:
                self._validate_history_table(schema, table, operation_timestamp)
            except ValueError as e:
                message = e.args[0]
                log_message(
                    LOG_WARNING,
                    f"[Migrate:DropColumnHistory] table={schema}.{table} column={column_name}: {message}",
                )
                return destination_sdk_pb2.MigrateResponse(
                    success=False,
                    warning=common_pb2.Warning(message=message),
                )

            # Compute lists of columns.
            all_columns, unchanged_columns = TableMetadataHelper.column_lists(
                table_obj, modulo_column_name=column_name
            )

            sql_bag = SqlBag()

            # Insert new rows to record the history of the DDL operation.
            # TODO: The `operation_timestamp` is directly interpolated into SQL strings.
            #       Consider using parameterized queries.
            sql_bag.add(f"""
            INSERT INTO "{schema}"."{table}" ({", ".join(all_columns)})
            (
              SELECT
                {", ".join(unchanged_columns)},
                NULL AS "{column_name}",
                '{operation_timestamp}'::TIMESTAMP AS {FIVETRAN_START}
              FROM "{schema}"."{table}"
              WHERE {FIVETRAN_ACTIVE} = TRUE
                AND "{column_name}" IS NOT NULL
                AND {FIVETRAN_START} < '{operation_timestamp}'::TIMESTAMP
            );
            """)

            # Update the newly added row with the `operation_timestamp`.
            sql_bag.add(f"""
            UPDATE "{schema}"."{table}"
            SET "{column_name}" = NULL
            WHERE {FIVETRAN_START} = '{operation_timestamp}'::TIMESTAMP;
            """)

            # Update the previous record's `_fivetran_end` to `(operation timestamp) - 1ms`
            # and set `_fivetran_active` to `FALSE`.
            sql_bag.add(f"""
            UPDATE "{schema}"."{table}"
               SET
                 {FIVETRAN_END} = '{operation_timestamp}'::TIMESTAMP - INTERVAL '1 millisecond',
                 {FIVETRAN_ACTIVE} = FALSE
               WHERE {FIVETRAN_ACTIVE} = TRUE
                 AND "{column_name}" IS NOT NULL
                 AND {FIVETRAN_START} < '{operation_timestamp}'::TIMESTAMP;
            """)

            # TODO: Review this: It mitigates a severe error raised by
            #       the Fivetran SDK tester, but is it actually intended?
            # INFO:   Fivetran-Tester-Process: Verifying if migration is success. Triggering describeTable for table: transaction_history
            # SEVERE: Fivetran-Tester-Process: Failed to process file: schema_migrations_input_sync_modes.json - Column 'desc' still exists after drop operation in history mode.
            sql_bag.add(f"""
            ALTER TABLE "{schema}"."{table}"
            DROP COLUMN "{column_name}";
            """)

            with self.engine.connect() as conn:
                sql_bag.execute(conn)

            log_message(
                LOG_INFO,
                f"[Migrate:DropColumnHistory] table={schema}.{table} column={drop_column.column} op_ts={drop_column.operation_timestamp}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        log_message(LOG_WARNING, "[Migrate:Drop] No drop entity specified")
        return destination_sdk_pb2.MigrateResponse(unsupported=True)

    def handle_copy(self, copy_op, schema, table, table_obj: common_pb2.Table):
        """Handles copy operations (copy table, copy column, copy table to history mode)."""
        entity_case = copy_op.WhichOneof("entity")

        if entity_case == "copy_table":
            copy_table = copy_op.copy_table
            sql = (
                f'CREATE TABLE "{schema}"."{copy_table.to_table}" '
                f'AS SELECT * FROM "{schema}"."{copy_table.from_table}"'
            )
            with self.engine.connect() as conn:
                conn.execute(sa.text(sql))

            log_message(
                LOG_INFO,
                f"[Migrate:CopyTable] from={copy_table.from_table} to={copy_table.to_table} in schema={schema}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if entity_case == "copy_column":
            sql_bag = SqlBag()
            copy_column = copy_op.copy_column
            for col in table_obj.columns:
                if col.name == copy_column.from_column:
                    new_col = type(col)()
                    new_col.CopyFrom(col)
                    new_col.name = copy_column.to_column
                    table_obj.columns.add().CopyFrom(new_col)
                    type_ = TypeMap.to_cratedb(new_col.type, new_col.params)
                    sql_bag.add(
                        f'ALTER TABLE "{schema}"."{table}" ADD COLUMN "{new_col.name}" {type_};'
                    )
                    sql_bag.add(f'UPDATE "{schema}"."{table}" SET "{new_col.name}"="{col.name}";')
                    break

            if sql_bag:
                with self.engine.connect() as conn:
                    sql_bag.execute(conn)

            log_message(
                LOG_INFO,
                f"[Migrate:CopyColumn] table={schema}.{table} from_col={copy_column.from_column} to_col={copy_column.to_column}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if entity_case == "copy_table_to_history_mode":
            # table-map manipulation to simulate copy table to history mode, replace with actual logic.
            copy_table_history_mode = copy_op.copy_table_to_history_mode
            if copy_table_history_mode.from_table in self.table_map:
                from_table_obj = self.table_map[copy_table_history_mode.from_table]
                new_table = TableMetadataHelper.create_table_copy(
                    from_table_obj, copy_table_history_mode.to_table
                )
                TableMetadataHelper.remove_column_from_table(
                    new_table, copy_table_history_mode.soft_deleted_column
                )
                TableMetadataHelper.add_history_mode_columns(new_table)
                self.table_map[copy_table_history_mode.to_table] = new_table

            log_message(
                LOG_INFO,
                f"[Migrate:CopyTableToHistoryMode] from={copy_table_history_mode.from_table} to={copy_table_history_mode.to_table} soft_deleted_column={copy_table_history_mode.soft_deleted_column}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        log_message(LOG_WARNING, "[Migrate:Copy] No copy entity specified")
        return destination_sdk_pb2.MigrateResponse(unsupported=True)

    def handle_rename(self, rename_op, schema, table):
        """Handles rename operations (rename table, rename column)."""
        entity_case = rename_op.WhichOneof("entity")

        if entity_case == "rename_table":
            rt = rename_op.rename_table
            sql = f'ALTER TABLE "{schema}"."{rt.from_table}" RENAME TO "{rt.to_table}";'
            with self.engine.connect() as conn:
                conn.execute(sa.text(sql))

            log_message(
                LOG_INFO,
                f"[Migrate:RenameTable] from={rt.from_table} to={rt.to_table} schema={schema}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if entity_case == "rename_column":
            rename_column = rename_op.rename_column
            sql = f'ALTER TABLE "{schema}"."{table}" RENAME "{rename_column.from_column}" TO "{rename_column.to_column}";'
            with self.engine.connect() as conn:
                conn.execute(sa.text(sql))

            log_message(
                LOG_INFO,
                f"[Migrate:RenameColumn] table={schema}.{table} from_col={rename_column.from_column} to_col={rename_column.to_column}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        log_message(LOG_WARNING, "[Migrate:Rename] No rename entity specified")
        return destination_sdk_pb2.MigrateResponse(unsupported=True)

    def handle_add(self, add_op, schema, table, table_obj: common_pb2.Table):
        """
        Handles add operations (add column in history mode, add column with default value).

        - https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#add_column_in_history_mode
        - https://github.com/fivetran/fivetran_partner_sdk/blob/main/schema-migration-helper-service.md#add_column_with_default_value
        """
        entity_case = add_op.WhichOneof("entity")

        # Add a column to history-mode tables while preserving historical record integrity.
        if entity_case == "add_column_in_history_mode":
            add_col_history_mode = add_op.add_column_in_history_mode

            column_name = add_col_history_mode.column
            column_type = TypeMap.to_cratedb(add_col_history_mode.column_type)
            default_value = add_col_history_mode.default_value
            operation_timestamp = add_col_history_mode.operation_timestamp

            sql_bag = SqlBag()

            # Validate table is non-empty and `max(_fivetran_start) < operation_timestamp`.
            try:
                self._validate_history_table(schema, table, operation_timestamp)
            except ValueError as e:
                message = e.args[0]
                log_message(
                    LOG_WARNING,
                    f"[Migrate:AddColumnHistory] table={schema}.{table} column={column_name}: {message}",
                )
                return destination_sdk_pb2.MigrateResponse(
                    success=False,
                    warning=common_pb2.Warning(message=message),
                )

            # Add the new column with the specified type.
            sql_bag.add(f"""
            ALTER TABLE "{schema}"."{table}" ADD COLUMN "{column_name}" {column_type};
            """)

            # Compute lists of columns.
            all_columns, unchanged_columns = TableMetadataHelper.column_lists(
                table_obj, modulo_column_name=column_name
            )

            # Insert new rows to record the history of the DDL operation.
            # TODO: `default_value` is directly interpolated without escaping. If it contains single
            #        quotes or other SQL metacharacters, this will cause syntax errors or injection.
            sql_bag.add(f"""
            INSERT INTO "{schema}"."{table}" ({", ".join(all_columns)})
            (
              SELECT
                {", ".join(unchanged_columns)},
                '{default_value}'::{column_type} AS "{column_name}",
                '{operation_timestamp}'::TIMESTAMP AS {FIVETRAN_START}
              FROM "{schema}"."{table}"
              WHERE {FIVETRAN_ACTIVE} = TRUE
                AND {FIVETRAN_START} < '{operation_timestamp}'::TIMESTAMP
            );
            """)

            # Update the newly added rows with the `default_value` and `operation_timestamp`.
            # TODO: Remove? Is it really needed? It looks redundant to the operation above.
            '''
            sql_bag.add(f"""
            UPDATE "{schema}"."{table}"
            SET "{column_name}" = '{default_value}',
                {FIVETRAN_START} = '{operation_timestamp}'
            WHERE {FIVETRAN_ACTIVE} = TRUE
              AND {FIVETRAN_START} = '{operation_timestamp}'
            """)
            '''

            # Deactivate original active records (those without the new column set),
            # by updating the previous active record's `_fivetran_end` to
            # `(operation timestamp) - 1ms` and set `_fivetran_active` to `FALSE`.
            sql_bag.add(f"""
            UPDATE "{schema}"."{table}"
            SET {FIVETRAN_END} = '{operation_timestamp}'::TIMESTAMP - INTERVAL '1 millisecond',
                {FIVETRAN_ACTIVE} = FALSE
            WHERE {FIVETRAN_ACTIVE} = TRUE
              AND {FIVETRAN_START} < '{operation_timestamp}'::TIMESTAMP;
            """)
            with self.engine.connect() as conn:
                sql_bag.execute(conn)

            log_message(
                LOG_INFO,
                f"[Migrate:AddColumnHistory] table={schema}.{table} column={add_col_history_mode.column} type={add_col_history_mode.column_type} default={add_col_history_mode.default_value} op_ts={add_col_history_mode.operation_timestamp}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        # Add a new column with a specified data type and default value.
        if entity_case == "add_column_with_default_value":
            add_col_default_with_value = add_op.add_column_with_default_value

            new_col = table_obj.columns.add()
            new_col.name = add_col_default_with_value.column
            new_col.type = add_col_default_with_value.column_type
            default_value = add_col_default_with_value.default_value
            type_ = TypeMap.to_cratedb(new_col.type, new_col.params)
            # FIXME: Improve after CrateDB does it right.
            #        - https://github.com/crate/cratedb-fivetran-destination/issues/111
            #        - https://github.com/crate/crate/issues/18783
            # sql = f'ALTER TABLE "{schema}"."{table}" ADD COLUMN "{new_col.name}" {type_} DEFAULT \'{default_value}\';'  # noqa: ERA001
            sql_bag = SqlBag()
            sql_bag.add(f'ALTER TABLE "{schema}"."{table}" ADD COLUMN "{new_col.name}" {type_};')
            if default_value is not None:
                sql_bag.add(
                    f'UPDATE "{schema}"."{table}" SET "{new_col.name}" = \'{default_value}\';'
                )
            with self.engine.connect() as conn:
                sql_bag.execute(conn)

            log_message(
                LOG_INFO,
                f"[Migrate:AddColumnDefault] table={schema}.{table} column={add_col_default_with_value.column} type={add_col_default_with_value.column_type} default={add_col_default_with_value.default_value}",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        log_message(LOG_WARNING, "[Migrate:Add] No add entity specified")
        return destination_sdk_pb2.MigrateResponse(unsupported=True)

    def handle_update_column_value(self, upd, schema, table):
        """Handles update column value operation."""
        with self.engine.connect() as conn:
            conn.execute(
                sa.text(f'UPDATE "{schema}"."{table}" SET "{upd.column}"=:value;'),
                parameters={"value": upd.value},
            )
            conn.execute(sa.text(f'REFRESH TABLE "{schema}"."{table}";'))

        log_message(
            LOG_INFO,
            f"[Migrate:UpdateColumnValue] table={schema}.{table} column={upd.column} value={upd.value}",
        )
        return destination_sdk_pb2.MigrateResponse(success=True)

    def handle_table_sync_mode_migration(self, op, schema, table):
        """Handles table sync mode migration operations."""
        table_obj = self.table_map.get(table)

        soft_deleted_column = op.soft_deleted_column if op.HasField("soft_deleted_column") else None

        # Determine the migration type and handle accordingly
        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.SOFT_DELETE_TO_LIVE:
            # table-map manipulation to simulate soft delete to live, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.remove_column_from_table(table_copy, soft_deleted_column)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from SOFT_DELETE to LIVE",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.SOFT_DELETE_TO_HISTORY:
            # table-map manipulation to simulate soft delete to history, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.remove_column_from_table(table_copy, soft_deleted_column)
            TableMetadataHelper.add_history_mode_columns(table_copy)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from SOFT_DELETE to HISTORY",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.HISTORY_TO_SOFT_DELETE:
            # table-map manipulation to simulate history to soft delete, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.remove_history_mode_columns(table_copy)
            TableMetadataHelper.add_soft_delete_column(table_copy, soft_deleted_column)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from HISTORY to SOFT_DELETE",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.HISTORY_TO_LIVE:
            # table-map manipulation to simulate history to live, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.remove_history_mode_columns(table_copy)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from HISTORY to LIVE",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.LIVE_TO_SOFT_DELETE:
            # table-map manipulation to simulate live to soft delete, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.add_soft_delete_column(table_copy, soft_deleted_column)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from LIVE to SOFT_DELETE",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        if op.type == destination_sdk_pb2.TableSyncModeMigrationType.LIVE_TO_HISTORY:
            # table-map manipulation to simulate live to history, replace with actual logic.
            table_copy = TableMetadataHelper.create_table_copy(table_obj, table_obj.name)
            TableMetadataHelper.add_history_mode_columns(table_copy)
            self.table_map[table] = table_copy

            log_message(
                LOG_INFO,
                f"[Migrate:TableSyncModeMigration] Migrating table={schema}.{table} from LIVE to HISTORY",
            )
            return destination_sdk_pb2.MigrateResponse(success=True)

        log_message(
            LOG_WARNING,
            f"[Migrate:TableSyncModeMigration] Unknown migration type for table={schema}.{table}",
        )
        return destination_sdk_pb2.MigrateResponse(unsupported=True)

    def _validate_history_table(self, schema, table, operation_timestamp):
        """
        Validate table is non-empty and `max(_fivetran_start) < operation_timestamp`.
        """
        with self.engine.connect() as conn:
            # Synchronize previous writes.
            conn.execute(sa.text(f'REFRESH TABLE "{schema}"."{table}";'))

            # Check for emptiness.
            cardinality = int(
                conn.execute(sa.text(f'SELECT COUNT(*) FROM "{schema}"."{table}";')).scalar_one()
            )
            if cardinality == 0:
                raise ValueError("table is empty")

            # Validate operation timestamp condition.
            sql = f"""
            SELECT TO_CHAR(MAX({FIVETRAN_START}), 'YYYY-MM-DDTHH:MI:SSZ') AS max_start
            FROM "{schema}"."{table}"
            WHERE {FIVETRAN_ACTIVE} = TRUE
            """
            max_start = conn.execute(sa.text(sql)).scalar_one()
            if max_start is not None and max_start >= operation_timestamp:
                raise ValueError(
                    f"`operation_timestamp` {operation_timestamp} must be after `max(_fivetran_start)` {max_start}"
                )


class TableMetadataHelper:
    """Helper class for table metadata operations"""

    @staticmethod
    def create_table_copy(table_obj, new_name):
        """Creates a copy of a table."""
        table_copy = table_obj.__class__.FromString(table_obj.SerializeToString())
        if hasattr(table_copy, "name"):
            table_copy.name = new_name
        return table_copy

    @staticmethod
    def remove_column_from_table(table_obj, column_name):
        """Removes a column from a table."""
        if not column_name or not hasattr(table_obj, "columns"):
            return
        # Create a new list of columns excluding the specified column
        columns_to_keep = [col for col in table_obj.columns if col.name != column_name]
        # Clear and repopulate
        del table_obj.columns[:]
        table_obj.columns.extend(columns_to_keep)

    @staticmethod
    def remove_history_mode_columns(table_obj):
        """Removes history mode columns from a table."""
        if not hasattr(table_obj, "columns"):
            return
        columns_to_keep = [
            col
            for col in table_obj.columns
            if col.name not in [FIVETRAN_START, FIVETRAN_END, FIVETRAN_ACTIVE]
        ]
        del table_obj.columns[:]
        table_obj.columns.extend(columns_to_keep)

    @staticmethod
    def add_history_mode_columns(table_obj):
        """Adds history mode columns to a table."""
        if not hasattr(table_obj, "columns"):
            return
        start_col = table_obj.columns.add()
        start_col.name = FIVETRAN_START
        start_col.type = common_pb2.DataType.UTC_DATETIME

        end_col = table_obj.columns.add()
        end_col.name = FIVETRAN_END
        end_col.type = common_pb2.DataType.UTC_DATETIME

        active_col = table_obj.columns.add()
        active_col.name = FIVETRAN_ACTIVE
        active_col.type = common_pb2.DataType.BOOLEAN

    @staticmethod
    def add_soft_delete_column(table_obj, column_name):
        """Adds a soft delete column to a table."""
        if not column_name or not hasattr(table_obj, "columns"):
            return
        soft_del_col = table_obj.columns.add()
        soft_del_col.name = column_name
        soft_del_col.type = common_pb2.DataType.BOOLEAN

    @classmethod
    def column_lists(
        cls, table_obj: common_pb2.Table, modulo_column_name: t.Optional[str] = None
    ) -> t.Tuple[t.List[str], t.List[str]]:
        """Return list of column names."""
        table_obj_tmp = deepcopy(table_obj)
        if modulo_column_name is not None:
            TableMetadataHelper.remove_column_from_table(table_obj_tmp, modulo_column_name)
        TableMetadataHelper.remove_column_from_table(
            table_obj_tmp, FieldMap.to_fivetran(FIVETRAN_START)
        )
        unchanged_columns = [f'"{FieldMap.to_cratedb(col.name)}"' for col in table_obj_tmp.columns]
        if modulo_column_name is not None:
            all_columns = [*unchanged_columns, f'"{modulo_column_name}"', FIVETRAN_START]
        else:
            all_columns = [*unchanged_columns, FIVETRAN_START]
        return all_columns, unchanged_columns
