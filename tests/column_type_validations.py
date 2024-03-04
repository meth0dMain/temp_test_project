from pandas import DataFrame

from validation import validate_column_type


def test_integer_validation_with_valid_data():
    df = DataFrame({"User ID": [1, 2, 3], "Integer Column": [100, 200, 300]})
    validated_df = validate_column_type(df, "integer_check", ["Integer Column"])

    assert len(df) == len(validated_df)
    assert validated_df["Integer Column"].isna().any() is not True


def test_integer_validation_with_invalid_data():
    df = DataFrame({"User ID": [1, 2, 3], "Integer Column": [100, "invalid", 300]})
    validated_df = validate_column_type(df, "integer_check", ["Integer Column"])

    assert len(validated_df) < len(df)
    assert validated_df["Integer Column"].dtype == int


def test_date_validation_with_valid_data():
    df = DataFrame(
        {"User ID": [1, 2, 3], "Date Column": ["01.01.2020", "02.02.2020", "03.03.2020"]}
    )
    validated_df = validate_column_type(df, "date_check", ["Date Column"])

    assert len(df) == len(validated_df)
    assert validated_df["Date Column"].isna().any() is not True


def test_date_validation_with_invalid_data():
    df = DataFrame({"User ID": [1, 2, 3], "Date Column": ["01.01.2020", "invalid", "03.03.2020"]})
    validated_df = validate_column_type(df, "date_check", ["Date Column"])

    assert len(validated_df) < len(df)


def test_invalid_column_type_raises_value_error():
    df = DataFrame({"User ID": [1, 2, 3], "Some Column": [100, 200, 300]})
    try:
        validate_column_type(df, "unsupported_check", ["Some Column"])
    except ValueError as e:
        assert str(e) == "Invalid column type. Please provide a valid column type."
