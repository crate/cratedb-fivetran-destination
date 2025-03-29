import re

import pytest
import sqlalchemy as sa

from cratedb_fivetran_destination import __version__
from cratedb_fivetran_destination.engine import Processor
from cratedb_fivetran_destination.model import TableInfo
from cratedb_fivetran_destination.sdk_pb2 import common_pb2
from cratedb_fivetran_destination.util import format_log_message, setup_logging


def test_version():
    assert __version__ >= "0.0.0"


def test_setup_logging():
    setup_logging(verbose=True)


def test_api_test(capsys):
    """
    Invoke gRPC API method `Test`.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method.
    config = {"url": "crate://"}
    response = destination.Test(
        request=common_pb2.TestRequest(name="foo", configuration=config),
        context=common_pb2.TestResponse(),
    )
    assert response.success is True
    assert response.failure == ""

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message("Test database connection: foo", newline=True)


def test_processor_failing(engine):
    table_info = TableInfo(fullname="foo.bar", primary_keys=["id"])
    p = Processor(engine=engine)
    with pytest.raises(sa.exc.ProgrammingError) as ex:
        p.process(
            table_info=table_info,
            upsert_records=[{"id": 1, "name": "Hotzenplotz"}],
            update_records=[{"id": 2}],
            delete_records=[{"id": 2}],
        )
    assert ex.match(re.escape("SchemaUnknownException[Schema 'foo' unknown]"))
