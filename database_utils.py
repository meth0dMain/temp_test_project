"""
Provides classes for managing SQL data insertions and database connections.
"""

import sqlite3
from typing import List, Optional, Tuple

from pandas import DataFrame


class SQLInsertionData:
    def __init__(
        self,
        df: DataFrame,
        table_name: str,
        columns: List[str],
        query: str,
        drop_duplicates: Optional[bool] = False,
    ):
        """
        Initializes the SQLDataPreparer instance.

        Args:
            df: The pandas DataFrame containing the data.
            table_name: The name of the target database table.
            columns: The list of column names to be included in the data.
            query: The SQL query string for inserting the data.
            drop_duplicates: Indicator to remove duplicates or not.
        """
        self.query = query
        self.data = self._prepare_data(df, columns, drop_duplicates)
        self.name = table_name

    def _prepare_data(self, df: DataFrame, columns: List[str], drop_duplicates: bool):
        """
        Prepares data for SQL insertion by converting a DataFrame into a list of tuples.

        Args:
            df: DataFrame to prepare data from.
            columns: The list of columns to include in the data.
            drop_duplicates: If True, duplicate rows based on the specified columns.
                will be removed from the data set before preparation.

        Returns:
            A list of tuples representing the data for SQL insertion.
        """
        df_selected = df[columns]
        if drop_duplicates:
            df_selected = df_selected.drop_duplicates().reset_index(drop=True)
        return list(df_selected.itertuples(index=False, name=None))


class DBConnectionManager:
    """This context manager is responsible for creating and closing connections with SQLite database"""

    def __init__(self, local_db_name: str):
        self.sqlite_db_name = local_db_name
        self.cursor = None
        self.connection = None

    def __enter__(self) -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
        self.connection = sqlite3.connect(self.sqlite_db_name)
        self.cursor = self.connection.cursor()

        return self.cursor, self.connection

    def __exit__(self, exc_type: str, exc_value: str, exc_traceback: str):
        self.cursor.close()
        self.connection.close()
