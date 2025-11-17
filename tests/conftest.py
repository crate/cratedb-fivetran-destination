import pytest
import sqlalchemy as sa


@pytest.fixture
def engine():
    engine = sa.create_engine("crate://")
    yield engine
    engine.dispose()
