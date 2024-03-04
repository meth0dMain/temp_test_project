from pandas import DataFrame

from validation import validate_column_data

valid_subscriptions = ["Basic", "Standard", "Premium"]


def test_validate_column_data_no_removal_needed():
    data = {
        "User ID": [1, 2, 3],
        "Subscription Type": ["Basic", "Standard", "Premium"]
    }
    df = DataFrame(data)
    validated_df = validate_column_data(df, "Subscription Type", valid_subscriptions)
    assert len(df) == len(validated_df)


def test_validate_column_data_removal_of_invalid_rows():
    data = {
        "User ID": [1, 2, 3, 4],
        "Subscription Type": ["Basic", "Standard", "Gold", "Silver"]
    }
    validated_df = validate_column_data(DataFrame(data), "Subscription Type", valid_subscriptions)
    expected_valid_rows = 2  # Only 'Basic' and 'Standard' are valid
    assert len(validated_df) == expected_valid_rows
