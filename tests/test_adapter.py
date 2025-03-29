import re

import pytest
import sqlalchemy as sa

from cratedb_fivetran_destination import __version__
from cratedb_fivetran_destination.engine import Processor
from cratedb_fivetran_destination.model import TableInfo
from cratedb_fivetran_destination.sdk_pb2 import common_pb2, destination_sdk_pb2
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


def test_api_configuration_form(capsys):
    """
    Invoke gRPC API method `ConfigurationForm`.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method.
    response = destination.ConfigurationForm(
        request=common_pb2.ConfigurationFormRequest(),
        context=common_pb2.ConfigurationFormResponse(),
    )

    # Extract field of concern.
    url_field: common_pb2.FormField = response.fields[3].conditional_fields.fields[0]

    # Validate fields.
    assert url_field.name == "url"
    assert "CrateDB database connection URL" in url_field.label

    # Validate tests.
    assert response.tests[0].name == "connect"

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message("Fetching configuration form", newline=True)


def test_api_describe_table_found(engine, capsys):
    """
    Invoke gRPC API method `DescribeTable` on an existing table.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    with engine.connect() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("CREATE TABLE testdrive.foo (id INT)"))

    # Invoke gRPC API method under test.
    config = {"url": "crate://"}
    response = destination.DescribeTable(
        request=destination_sdk_pb2.DescribeTableRequest(
            table_name="foo", schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.DescribeTableResponse(),
    )

    # Validate outcome.
    assert response.not_found is False
    assert response.warning.message == ""
    assert response.table == common_pb2.Table(
        name="foo",
        columns=[
            common_pb2.Column(
                name="id",
                type=common_pb2.DataType.INT,
                primary_key=False,
            )
        ],
    )

    # Check log output.
    out, err = capsys.readouterr()
    assert "Completed fetching table info" in out


def test_api_describe_table_not_found(capsys):
    """
    Invoke gRPC API method `DescribeTable` on an existing table.
    """
    from cratedb_fivetran_destination.main import CrateDBDestinationImpl

    destination = CrateDBDestinationImpl()

    # Invoke gRPC API method under test.
    config = {"url": "crate://"}
    response = destination.DescribeTable(
        request=destination_sdk_pb2.DescribeTableRequest(
            table_name="unknown", schema_name="testdrive", configuration=config
        ),
        context=destination_sdk_pb2.DescribeTableResponse(),
    )

    # Validate outcome.
    assert response.not_found is False
    assert response.warning.message == "Table not found: unknown"
    assert response.table.name == ""
    assert response.table.columns == []

    # Check log output.
    out, err = capsys.readouterr()
    assert out == format_log_message(
        "DescribeTable: Table not found: unknown", level="WARNING", newline=True
    )


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
