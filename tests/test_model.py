import re

import pytest

from cratedb_fivetran_destination.model import SqlBag


def test_sqlbag(engine):
    bag = SqlBag().add("SELECT 23").add("SELECT 42")
    with engine.connect() as connection:
        bag.execute(connection)


def test_sqlbag_add_none():
    with pytest.raises(TypeError) as excinfo:
        SqlBag().add(None)
    excinfo.match(re.escape("Input SQL must be str or SqlBag, not <class 'NoneType'>"))
