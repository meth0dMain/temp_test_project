import unittest
from unittest.mock import patch

import pytest
from pandas import DataFrame

from database_utils import DBConnectionManager, SQLInsertionData

df = DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
table_name = "users"
query = "INSERT INTO users (id, name) VALUES (?, ?)"
columns = ["id", "name"]


def test_insertion_data_creation_success():
    sql_insertion_data = SQLInsertionData(df, table_name, columns, query, drop_duplicates=False)
    assert sql_insertion_data.query == query
    assert sql_insertion_data.name == table_name
    assert sql_insertion_data.data == [(1, "Alice"), (2, "Bob"), (3, "Charlie")]


def test_insertion_data_creation_failure():
    df_empty = DataFrame()
    with pytest.raises(KeyError):
        SQLInsertionData(df_empty, table_name, columns, query, drop_duplicates=False)


def test_failure_on_incorrect_column_names_in_insertion_data():
    incorrect_columns = ["id", "nms"]  # 'nms' does not exist in the DataFrame
    with pytest.raises(KeyError):
        SQLInsertionData(df, table_name, incorrect_columns, query, drop_duplicates=False)


class TestDBConnectionManager(unittest.TestCase):
    @patch("database_utils.sqlite3")
    def test_connection_management(self, mock_sqlite):
        db_name = "test.db"
        manager = DBConnectionManager(db_name)
        with manager as (cursor, connection):
            self.assertIsNotNone(cursor)
            self.assertIsNotNone(connection)
        mock_sqlite.connect.assert_called_with(db_name)
        connection.cursor.assert_called()
        cursor.close.assert_called()
        connection.close.assert_called()
