from database_operations import create_tables_in_db, insert_data_to_db, prepare_sql_insertion_data
from utils.csv import create_df_from_csv
from utils.log_config import init_logger
from utils.parser import parse_arguments
from validation import dataframe_validation


def complete_assignment(dataset_name: str, database_name: str) -> None:
    """
    Process a NetFlix dataset for a 'Data Engineer Take Home Task' project by loading it, validating the data,
    creating necessary database tables, preparing the data for SQL insertion, and inserting the data into a database.

    This function orchestrates the workflow of data preparation and insertion by:
    1. Loading the dataset from a CSV file.
    2. Validating the loaded DataFrame to ensure data integrity.
    3. Creating tables in the specified database to accommodate the data.
    4. Preparing the validated data for SQL insertion.
    5. Inserting the prepared data into the database.

    Args:
        dataset_name: The name of the dataset file (CSV) to be processed.
        database_name: The name of the database where the data will be inserted.
    """
    netflix_df = create_df_from_csv(dataset_name)
    netflix_df = dataframe_validation(netflix_df)
    create_tables_in_db(db_name)
    data_to_insert = prepare_sql_insertion_data(netflix_df)
    insert_data_to_db(db_name, data_to_insert)


if __name__ == "__main__":
    LOGGER = init_logger(logger_name="inBank assignment")
    dataset, db_name = parse_arguments()
    complete_assignment(dataset, db_name)
