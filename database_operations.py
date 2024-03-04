"""
Handles database table creation, data preparation for SQL insertion, and data insertion processes.
"""

import logging
from typing import List

from pandas import DataFrame

from database_utils import DBConnectionManager, SQLInsertionData
from sql_queries.insertions import *
from sql_queries.table import *

LOGGER = logging.getLogger(__name__)


def create_tables_in_db(db_name: str) -> None:
    """Create the necessary tables in a SQLite database for storing data."""

    list_of_tables_to_create = [
        USERS_TABLE,
        SUBSCRIPTIONS_TABLE,
        DEVICES_TABLE,
        USER_DEVISES_TABLE,
        VIEWING_ACTIVITY_TABLE,
        PROFILES_TABLE,
    ]
    with DBConnectionManager(db_name) as (cursor, conn):
        for table_statement in list_of_tables_to_create:
            cursor.execute(table_statement)
            conn.commit()
    LOGGER.info("Tables have been created.")


def prepare_sql_insertion_data(df: DataFrame) -> List[SQLInsertionData]:
    """
    Prepare data for SQL insertion by specifying the relevant DataFrame columns and SQL queries for each table.

    Args:
        df: The source DataFrame containing all necessary data.

    Returns:
        A list of SQLDataPreparer objects, each configured for a specific table's data preparation and insertion.
    """
    user_data = SQLInsertionData(
        df, table_name="users", columns=["User ID", "Age", "Gender", "Country"], query=INSERT_USERS
    )
    subscription_data = SQLInsertionData(
        df,
        table_name="subscriptions",
        columns=[
            "User ID",
            "Subscription Type",
            "Monthly Revenue",
            "Join Date",
            "Last Payment Date",
            "Plan Duration",
        ],
        query=INSERT_SUBSCRIPTION,
    )
    device_data = SQLInsertionData(
        df, table_name="devices", columns=["Device"], query=INSERT_DEVICE, drop_duplicates=True
    )

    viewing_activity_data = SQLInsertionData(
        df,
        table_name="viewing_activity",
        columns=["User ID", "Movies Watched", "Series Watched"],
        query=INSERT_VIEWING_ACTIVITY,
    )
    user_profiles_data = SQLInsertionData(
        df,
        table_name="profiles",
        columns=["User ID", "Active Profiles", "Household Profile Ind"],
        query=INSERT_PROFILE,
    )
    user_device_data = SQLInsertionData(
        df, table_name="user_devices", columns=["User ID", "Device"], query=INSERT_USER_DEVICE
    )
    return [
        user_data,
        subscription_data,
        device_data,
        viewing_activity_data,
        user_profiles_data,
        user_device_data,
    ]


def insert_data_to_db(db_name: str, tables_data: List[SQLInsertionData]) -> None:
    """
    Insert data into specified database tables. Utilizes a list of SQLInsertionData objects, each containing a SQL query
    and the corresponding data, to insert records into the database tables specified within each object.

    Args:
        db_name: The name or path of the database file.
        tables_data: A list of objects containing the data and queries for insertion.

    Raises:
        Exception: General exception for catching errors during database operations, such as insertion failures.
    """
    *all_other_tables, user_devices_data = tables_data
    try:
        with DBConnectionManager(db_name) as (cursor, conn):
            for table in all_other_tables:
                cursor.executemany(table.query, table.data)
                conn.commit()
                LOGGER.info(f"The data inserted to '{table.name}' successfully.")
    except Exception as e:
        LOGGER.error(f"Failed to insert data into '{table.name}': {e}")
        raise
    insert_user_device_data(user_devices_data, db_name)


def insert_user_device_data(user_device_data: SQLInsertionData, db_name: str) -> None:
    """
    Insert data into 'user_devices' table. Unlike other tables, 'user_devices' needs data from external table.
    After gathering 'device_id' and 'device_name', it can map the user_id with device_id.

    Args:
        user_device_data: User device data and query for insertion.
        db_name: The name or path of the database file.

    Raises:
         Exception: General exception for catching errors during database operations, such as insertion failures.
    """
    try:
        with DBConnectionManager(db_name) as (cursor, conn):
            cursor.execute("SELECT device_id, device_name FROM devices;")
            devices = cursor.fetchall()
            device_name_to_id = {device_name: device_id for device_id, device_name in devices}
            user_device_pairs = [
                (user_id, device_name_to_id[device_name])
                for user_id, device_name in user_device_data.data
            ]
            cursor.executemany(user_device_data.query, user_device_pairs)
            conn.commit()
            LOGGER.info(f"The data inserted to '{user_device_data.name}' successfully.")
    except Exception as e:
        LOGGER.error(f"Failed to insert data into '{user_device_data.name}': {e}")
        raise
