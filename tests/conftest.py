import pytest
import sqlalchemy as sa


@pytest.fixture
def engine():
    return sa.create_engine("crate://")
