import re

import pytest

from cratedb_fivetran_destination.model import SqlBag


def test_sqlbag(engine):
    bag = SqlBag().add("SELECT 23").add("SELECT 42")
    with engine.connect() as connection:
        bag.execute(connection)


def test_sqlbag_add_wrong_none():
    bag = SqlBag().add(None)
    assert bool(bag) is False


def test_sqlbag_add_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        SqlBag().add(42)
    excinfo.match(re.escape('Input SQL must be str or SqlBag, not "int"'))
