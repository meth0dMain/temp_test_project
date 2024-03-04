import pandas as pd


def create_df_from_csv(file_name: str) -> pd.DataFrame:
    """
    Create a DataFrame from a CSV file.

    Args:
        file_name: The name of the CSV file.

    Returns:
        A DataFrame with columns where unnecessary spaces have been removed.
    """
    file_path = f'./datasets/{file_name}'
    df = pd.read_csv(file_path, delimiter=';')
    df.columns = df.columns.str.strip()

    return df
