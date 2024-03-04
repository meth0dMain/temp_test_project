"""
Create a new deployment
    prefect deployment build prefect_flow.py:data_engineer_position -n complete_assignment
Execute it, and it will appear on the prefect UI.
    prefect deployment run 'data-engineer-position/complete_assignment
"""


from prefect import flow, get_run_logger

from main import complete_assignment


@flow(log_prints=True)
def data_engineer_position(dataset_name: str, database_name: str) -> None:
    """The following flow starts 'complete_assignment' - An InBank test task for a data engineer position.

    Args:
        dataset_name: The name of the dataset file (CSV) to be processed.
        database_name: The name of the database where the data will be inserted.
    """
    logger = get_run_logger()
    logger.info("starting the run")
    complete_assignment(dataset_name, database_name)


if __name__ == "__main__":
    data_engineer_position.serve(
        name="daily_netflix_elt",
        tags=["test_assignment"],
        parameters={
            "dataset_name": "Netflix_dataset.csv",
            "database_name": "inbank_local.db"
        },
        cron="0 12 * * *",
    )
