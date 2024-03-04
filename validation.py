"""
Contains validations definitions.
"""

import logging
from typing import List

import pandas as pd

from constants import *

LOGGER = logging.getLogger(__name__)


def validate_ages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the 'Age' column in the DataFrame by removing incorrect data.

    Notes:
        Customers must be at least 18 years old to create a Netflix account due to age restrictions for
        certain content and legal requirements for accounts with financial responsibilities.

    Args:
        df: DataFrame to be validated.

    Returns:
        A filtered DataFrame after removing rows with incorrect 'Age' values.
    """
    valid_age_range = (18, 130)
    invalid_rows = df[~df["Age"].between(valid_age_range[0], valid_age_range[1])]
    if not invalid_rows.empty:
        LOGGER.warning("The following records will be removed due to incorrect Age:")
        LOGGER.warning(f"invalid_rows[['User ID', 'Age']]")
    filtered_df = df[df["Age"].between(valid_age_range[0], valid_age_range[1])]

    return filtered_df


def validate_payment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate payment records in the DataFrame by ensuring the 'Join Date' is always greater than the
    'Last Payment Date'. Invalid rows will be removed.

    Notes:
        Netflix does not offer free trials, so "Join Date" must always be greater than "Last Payment Date".

    Args:
        df: DataFrame containing payment records to be validated.

    Returns:
        A Filtered DataFrame after removing rows with incorrect payment records.
    """
    join_date_col = "Join Date"
    last_payment_date_col = "Last Payment Date"

    invalid_rows = df[df[join_date_col] > df[last_payment_date_col]]
    if not invalid_rows.empty:
        LOGGER.warning(
            f"The following records will be removed due to incorrect {join_date_col}and last_payment_date_col records:"
        )
        LOGGER.warning(invalid_rows[["User ID", join_date_col, last_payment_date_col]])
    df = df.drop(invalid_rows.index)

    return df


def validate_column_data(df: pd.DataFrame, column: str, valid_answers: List[str]) -> pd.DataFrame:
    """
    Validate a specific column in a DataFrame by removing rows with incorrect data.

    Args:
        df: The DataFrame to be validated.
        column: Column to compare.
        valid_answers: List of acceptable answers in the column.

    Returns:
         A filtered DataFrame after removing rows with incorrect data in the specified column.
    """
    rows_to_drop = df[~df[column].isin(valid_answers)]
    if not rows_to_drop.empty:
        LOGGER.warning(f"The following records will be removed due to incorrect {column} records:")
        LOGGER.warning(rows_to_drop[["User ID", column]])
    filtered_df = df[df[column].isin(valid_answers)]

    return filtered_df


def validate_column_type(df: pd.DataFrame, column_type: str, columns: List[str]) -> pd.DataFrame:
    """
    Validate and process columns in a DataFrame based on the specified column type.

    Args:
        df: The DataFrame to be validated.
        column_type: The type of validation to perform ("integer_check" or "date_check")
        columns: List of column names to be validated.

    Returns:
        A DataFrame after removing rows with data type inconsistencies.

    Raises:
        ValueError: If an invalid column type is provided.
    """
    if column_type == "integer_check":
        for column in columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
            non_integer_rows = df[df[column].isna()]
            if not non_integer_rows.empty:
                LOGGER.warning(f"Rows with non-integer values in {column} column:")
                LOGGER.warning(non_integer_rows[["User ID", column]])
            df = df.dropna(subset=[column], inplace=False)
            df[column] = df[column].astype(int)  # as pd.to_numeric converts column to float
    elif column_type == "date_check":
        for column in columns:
            df[column] = pd.to_datetime(df[column], errors="coerce", format="%d.%m.%Y")
            non_datetime_rows = df[df[column].isna()]
            if not non_datetime_rows.empty:
                LOGGER.warning(f"Rows with non-datetime values in {column} column:")
                LOGGER.warning(non_datetime_rows[["User ID", column]])
            df = df.dropna(subset=[column], inplace=False)
            df[column] = df[column].dt.date  # as pd.to_datetime converts column to datetime
    else:
        raise ValueError("Invalid column type. Please provide a valid column type.")
    return df


def dataframe_validation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the integrity of a DataFrame obtained from a CSV file by performing data and type validations.

    Args:
        df: The DataFrame to be validated.

    Returns:
        A filtered DataFrame after removing rows with incorrect data.
    """
    data_validations = {
        "Subscription Type": VALID_SUBSCRIPTION_TYPES,
        "Device": VALID_DEVICES,
        "Gender": VALID_GENDERS,
        "Country": VALID_COUNTRIES,
    }
    for k, v in data_validations.items():
        df = validate_column_data(df, column=k, valid_answers=v)

    type_validations = {"integer_check": INT_COLUMNS, "date_check": DATE_COLUMNS}
    for k, v in type_validations.items():
        df = validate_column_type(df, column_type=k, columns=v)
    df = validate_ages(df)
    df = validate_payment(df)
    LOGGER.info("Dataset has been validated")

    return df
