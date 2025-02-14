from cratedb_fivetran_destination import __version__
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
        out
        == '{"level":"INFO", "message": "test name: foo", "message-origin": "sdk_destination"}\n'
    )
