import typing as t

import sqlalchemy as sa
from attr import Factory
from attrs import define
from sqlalchemy_cratedb import ObjectType
from tikray.util.dictx import OrderedDictX

from cratedb_fivetran_destination.sdk_pb2.common_pb2 import DataType


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


class TypeMap:
    """
    Map Fivetran types to CrateDB types and back.
    """

    cratedb_default = sa.Text()
    fivetran_default = DataType.UNSPECIFIED

    fivetran_map = {
        DataType.UNSPECIFIED: sa.Text(),
        DataType.BOOLEAN: sa.Boolean(),
        DataType.SHORT: sa.Integer(),
        DataType.INT: sa.Integer(),
        DataType.LONG: sa.BigInteger(),
        DataType.FLOAT: sa.Float(),
        DataType.DOUBLE: sa.Double(),
        DataType.NAIVE_DATE: sa.Date(),
        DataType.NAIVE_DATETIME: sa.DateTime(),
        DataType.UTC_DATETIME: sa.DateTime(),
        DataType.DECIMAL: sa.DECIMAL(),
        DataType.BINARY: sa.Text(),
        DataType.STRING: sa.String(),
        DataType.JSON: ObjectType,
        DataType.XML: sa.String(),
        DataType.NAIVE_TIME: sa.DateTime(),
    }

    cratedb_map = {
        sa.String: DataType.STRING,
        sa.Text: DataType.STRING,
        sa.Boolean: DataType.BOOLEAN,
        sa.Integer: DataType.INT,
        sa.BigInteger: DataType.LONG,
        sa.Float: DataType.FLOAT,
        sa.Double: DataType.DOUBLE,
        sa.Date: DataType.NAIVE_DATE,
        # FIXME: Which one to choose?
        #        Need better inspection about aware/unaware datetime objects?
        sa.DateTime: DataType.NAIVE_DATETIME,
        # sa.DateTime: DataType.UTC_DATETIME,
        sa.DECIMAL: DataType.DECIMAL,
        sa.BINARY: DataType.BINARY,
        ObjectType: DataType.JSON,
    }

    @classmethod
    def fivetran_to_cratedb(cls, fivetran_type):
        return cls.fivetran_map.get(fivetran_type, cls.cratedb_default)

    @classmethod
    def cratedb_to_fivetran(cls, cratedb_type):
        return cls.cratedb_map.get(type(cratedb_type), cls.fivetran_default)


class FivetranKnowledge:
    """
    Manage special knowledge about Fivetran.

    Fivetran uses special values for designating NULL and CDC-unmodified values.
    """

    NULL_STRING = "null-m8yilkvPsNulehxl2G6pmSQ3G3WWdLP"
    UNMODIFIED_STRING = "unmod-NcK9NIjPUutCsz4mjOQQztbnwnE1sY3"

    @classmethod
    def replace_values(cls, record):
        rm_list = []
        for key, value in record.items():
            if value == cls.NULL_STRING:
                record[key] = None
            elif value == cls.UNMODIFIED_STRING:
                rm_list.append(key)
        for rm in rm_list:
            record.pop(rm)


@define
class TableInfo:
    fullname: str
    primary_keys: t.List[str] = Factory(list)
