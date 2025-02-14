import logging
import typing as t
from textwrap import dedent

import sqlalchemy as sa
from attr import Factory
from attrs import define
from tikray.util.dictx import OrderedDictX
from toolz import dissoc

from cratedb_fivetran_destination.sdk_pb2.common_pb2 import DataType

logger = logging.getLogger()


class CrateDBKnowledge:
    """
    Manage special knowledge about CrateDB.
    """

    # Map special column names, because CrateDB does not allow `_` prefixes.
    field_map = {
        "_fivetran_id": "__fivetran_id",
        "_fivetran_synced": "__fivetran_synced",
        "_fivetran_deleted": "__fivetran_deleted",
    }

    # Map Fivetran types to CrateDB types.
    # FIXME: Add more type mappings.
    # Status: 10%
    default_type = sa.Text()
    type_map = {
        DataType.INT: sa.Integer(),
    }

    @classmethod
    def rename_keys(cls, record):
        """
        Rename keys according to field map.
        """
        record = OrderedDictX(record)
        for key, value in cls.field_map.items():
            if key in record:
                record.rename_key(key, value)
        return record

    @classmethod
    def resolve_field(cls, fivetran_field):
        return cls.field_map.get(fivetran_field, fivetran_field)

    @classmethod
    def resolve_type(cls, fivetran_type):
        return cls.type_map.get(fivetran_type, cls.default_type)


@define
class TableInfo:
    fullname: str
    primary_keys: t.List[str] = Factory(list)


@define
class UpsertStatement:
    """
    Manage and render an SQL upsert statement suitable for CrateDB.

    INSERT INTO ... ON CONFLICT ... DO UPDATE SET ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    @property
    def data(self):
        """
        The full record without primary key data.
        """
        return dissoc(self.record, *self.table.primary_keys)

    def to_sql(self):
        """
        Render statement to SQL.
        """
        return dedent(f"""
        INSERT INTO {self.table.fullname}
        ({", ".join([f'"{key}"' for key in self.record.keys()])})
        VALUES ({", ".join([f":{key}" for key in self.record.keys()])})
        ON CONFLICT ({", ".join(self.table.primary_keys)}) DO UPDATE
        SET {", ".join([f'"{key}"="excluded"."{key}"' for key in self.data.keys()])}
        """)  # noqa: S608


@define
class UpdateStatement:
    """
    Manage and render an SQL update statement.

    UPDATE ... SET ... WHERE ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    @property
    def data(self):
        """
        The full record without primary key data.
        """
        return dissoc(self.record, *self.table.primary_keys)

    def to_sql(self):
        """
        Render statement to SQL.
        """
        return dedent(f"""
        UPDATE {self.table.fullname}
        SET {", ".join([f'"{key}" = :{key}' for key in self.data.keys()])}
        WHERE {" AND ".join([f'"{key}" = :{key}' for key in self.table.primary_keys])}
        """)  # noqa: S608


@define
class DeleteStatement:
    """
    Manage and render an SQL delete statement.

    DELETE FROM ... WHERE ...
    """

    table: TableInfo
    record: t.Dict[str, t.Any] = Factory(dict)

    def to_sql(self):
        """
        Render statement to SQL.
        """
        return dedent(f"""
        DELETE FROM {self.table.fullname}
        WHERE {" AND ".join([f'"{key}" = :{key}' for key in self.table.primary_keys])}
        """)  # noqa: S608


@define
class Processor:
    engine: sa.Engine

    def process(
        self,
        table_info: TableInfo,
        upsert_records: t.Generator[t.Dict[str, t.Any], None, None],
        update_records: t.Generator[t.Dict[str, t.Any], None, None],
        delete_records: t.Generator[t.Dict[str, t.Any], None, None],
    ):
        with self.engine.connect() as connection:
            # Apply upsert SQL statements.
            # `INSERT INTO ... ON CONFLICT ... DO UPDATE SET ...`.
            self.process_records(
                connection,
                upsert_records,
                lambda record: UpsertStatement(table=table_info, record=record).to_sql(),
            )

            self.process_records(
                connection,
                update_records,
                lambda record: UpdateStatement(table=table_info, record=record).to_sql(),
            )

            self.process_records(
                connection,
                delete_records,
                lambda record: DeleteStatement(table=table_info, record=record).to_sql(),
            )

    def process_records(self, connection, records, converter):
        for record in records:
            sql = converter(record)
            try:
                connection.execute(sa.text(sql), record)
            except sa.exc.ProgrammingError as ex:
                logger.exception(f"Processing database operation failed: {ex}")
                raise
