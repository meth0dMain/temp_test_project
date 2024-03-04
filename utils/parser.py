from argparse import ArgumentParser


def parse_arguments() -> tuple[str, str]:
    """Parses command-line arguments for the dataset and database names.

    Returns:
        A tuple containing the names of the dataset and database as strings.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--dataset_name",
        type=str,
        default="Netflix_dataset.csv",
        help="Specify the name of the dataset file to be processed",
    )
    parser.add_argument(
        "--database_name",
        type=str,
        default="inbank_local.db",
        help="Specify the name of the database file to be created or updated",
    )
    namespace = parser.parse_args()

    return namespace.dataset_name, namespace.database_name
