import re

import pytest
import sqlalchemy as sa

from cratedb_fivetran_destination import __version__
from cratedb_fivetran_destination.engine import Processor
from cratedb_fivetran_destination.main import setup_logging
from cratedb_fivetran_destination.model import TableInfo
from cratedb_fivetran_destination.sdk_pb2 import common_pb2


def test_dummy():
    assert 42 == 42


def test_version():
    assert __version__ >= "0.0.0"


def test_destination(capsys):
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke test function.
    config = {}
    config["url"] = "crate://"
    response = destination.Test(
        request=common_pb2.TestRequest(name="foo", configuration=config),
        context=common_pb2.TestResponse(),
    )
    assert response.success is True

    # Check stdout.
    out, err = capsys.readouterr()
    assert (
        out == '{"level":"INFO", "message": "Test database connection: foo", '
        '"message-origin": "sdk_destination"}\n'
    )


def test_setup_logging():
    setup_logging(verbose=True)


def test_processor_failing():
    table_info = TableInfo(fullname="foo.bar", primary_keys=["id"])
    engine = sa.create_engine("crate://localhost:4200/")
    p = Processor(engine=engine)
    with pytest.raises(sa.exc.ProgrammingError) as ex:
        p.process(
            table_info=table_info,
            upsert_records=[{"id": 1, "name": "Hotzenplotz"}],
            update_records=[{"id": 2}],
            delete_records=[{"id": 2}],
        )
    assert ex.match(re.escape("SchemaUnknownException[Schema 'foo' unknown]"))
