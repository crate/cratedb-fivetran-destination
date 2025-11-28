import pytest
import sqlalchemy as sa


@pytest.fixture
def engine():
    engine = sa.create_engine("crate://")
    with engine.connect() as conn:
        # Clean up stale "read-only" mode states.
        try:
            conn.execute(sa.text('ALTER TABLE testdrive.foo RESET ("blocks.write");'))
        except Exception:  # noqa: S110
            pass
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo"))
        conn.execute(sa.text("DROP TABLE IF EXISTS testdrive.foo_alter_tmp"))
    yield engine
    engine.dispose()
