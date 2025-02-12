from cratedb_fivetran_destination import __version__


def test_dummy():
    assert 42 == 42


def test_version():
    assert __version__ >= "0.0.0"
