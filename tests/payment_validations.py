import pandas as pd

from validation import validate_payment


def test_validate_payment_did_not_remove_any_rows():
    data = {
        "User ID": [1, 2, 3],
        "Join Date": ["2020-01-01", "2021-01-01", "2022-01-01"],
        "Last Payment Date": ["2020-12-31", "2021-12-31", "2022-12-31"]
    }
    df = pd.DataFrame(data)
    df["Join Date"] = pd.to_datetime(df["Join Date"])
    df["Last Payment Date"] = pd.to_datetime(df["Last Payment Date"])
    validated_df = validate_payment(df)

    assert len(df) == len(validated_df)


def test_validate_payment_did_remove_invalid_rows():
    data = {
        "User ID": [1, 2, 3, 4],
        "Join Date": ["2020-01-02", "2021-01-02", "2022-01-01", "2022-01-01"],
        "Last Payment Date": ["2020-01-01", "2021-01-01", "2022-01-02", "2021-12-31"]
    }
    df = pd.DataFrame(data)
    df["Join Date"] = pd.to_datetime(df["Join Date"])
    df["Last Payment Date"] = pd.to_datetime(df["Last Payment Date"])
    validated_df = validate_payment(df)
    expected_valid_rows = 1  # Only one row should remain after filtering

    assert len(validated_df) == expected_valid_rows
