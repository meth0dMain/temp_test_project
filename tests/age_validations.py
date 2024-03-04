from pandas import DataFrame

from validation import validate_ages


def test_validate_ages_did_not_remove_any_rows():
    data = {"User ID": [1, 2, 3], "Age": [25, 35, 45]}
    df = DataFrame(data)
    validated_df = validate_ages(df)

    assert len(df) == len(validated_df)


def test_validate_ages_did_remove_invalid_rows():
    data = {"User ID": [1, 2, 3, 4], "Age": [25, 35, 150, 5]}  # Ages 150 and 5 are invalid
    df = DataFrame(data)
    validated_df = validate_ages(df)
    expected_valid_rows = 2

    assert len(validated_df) == expected_valid_rows
