from cratedb_fivetran_destination.engine import EarliestStartHistoryStatements
from cratedb_fivetran_destination.model import TableInfo


def test_earliest_start_history_statements():
    eshs = EarliestStartHistoryStatements(table=TableInfo("foo.bar"), records=[])
    assert eshs.hard_delete_with_timestamp() is None
