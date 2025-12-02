import pytest
import sqlalchemy as sa
from sqlalchemy.testing.util import drop_all_tables


@pytest.fixture
def engine():
    engine = sa.create_engine("crate://")
    with engine.connect() as connection:
        inspector = sa.inspect(connection)
        unblock_all_tables(engine, inspector, schema="testdrive")
        drop_all_tables(engine, inspector, schema="testdrive")
    yield engine
    engine.dispose()


def unblock_all_tables(engine: sa.Engine, inspector: sa.Inspector, schema: str):
    """
    Clean up stale "read-only" mode states of all tables in schema.
    """
    with engine.begin() as connection:
        tables = inspector.get_table_names(schema=schema)
        for table in tables:
            connection.execute(sa.text(f'ALTER TABLE "{schema}"."{table}" RESET ("blocks.write");'))
