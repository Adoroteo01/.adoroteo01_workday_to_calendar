import pytest
from pandas import DataFrame, read_excel

from src.packages.converter.transform import (
    _find_end,
    _find_start,
    _no_header_df,
    import_data,
)


def get_test_data():
    """Returns a list of tuples containing the test data

    tuple values are meant for the read_excel function:
    read_excel(data, skiprows=x, skipfooter=y)
    where data is tuple[0], x is tuple[1], and y is tuple[2]

    """
    return [
        ("data/View_My_Courses_1.xlsx", 2, 0),
        ("data/View_My_Courses_2.xlsx", 5, 7),
        ("data/View_My_Courses_3.xlsx", 2, 0),
    ]


@pytest.fixture(params=get_test_data())
def test_data(request):
    return request.param


@pytest.fixture
def expected(test_data):
    """returns expected value for a schedule in test_data"""
    data, start, end = test_data
    return read_excel(data, skiprows=start, skipfooter=end)


@pytest.fixture
def start(test_data):
    """returns the index of the start of the ubc schedule"""
    return test_data[1]


@pytest.fixture
def end(test_data):
    """returns the index of the end of the ubc schedule"""
    return test_data[2]


@pytest.fixture
def data_path(test_data):
    """returns the path of a schedule in test_data"""
    return test_data[0]


@pytest.fixture
def data_dataframe(test_data):
    """returns a dataframe from a schedule path"""
    return read_excel(test_data[0])


# Test the case where a file path is passed to import_data
def test_import_data_path(data_path, expected):
    assert import_data(data_path).equals(expected)


# Test the case where a DataFrame is passed to import_data
def test_import_data_dataframe(data_dataframe, expected):
    assert import_data(data_dataframe).equals(expected)


# Test the case where a file path is passed to _find_start
def test_find_start_path(data_path, start):
    assert _find_start(data_path) == start


# Test the case where a DataFrame is passed to _find_start
def test_find_start_dataframe(data_dataframe, start):
    x = _find_start(data_dataframe)
    assert x == start


# Test the case where a file path is passed to _find_end
def test_find_end_path(data_path, end):
    assert _find_end(data_path) == end


# Test the case where a DataFrame is passed to _find_end
def test_find_end_dataframe(data_dataframe, end):
    assert _find_end(data_dataframe) == end


# test the case where an empty DataFrame is passed
def test_no_header_df_empty():

    dataframe = DataFrame({})

    expected = DataFrame({})
    result = _no_header_df(dataframe)

    assert expected.equals(result)


# tests the case where a 1x1 dataframe is passed
def test_no_header_df_1x1():

    dataframe = DataFrame({"x": [1], "y": [2]})

    expected = DataFrame({0: ["x", 1], 1: ["y", 2]})
    result = _no_header_df(dataframe)

    assert expected.equals(result)


# tests the case where a 2x3 dataframe is passed
def test_no_header_df_2x3():

    dataframe = DataFrame({"x": [1, 2], "y": [3, 4]})

    expected = DataFrame({0: ["x", 1, 2], 1: ["y", 3, 4]})
    result = _no_header_df(dataframe)

    assert expected.equals(result)


# TODO: !!! add tests for when users download during sem 1 versus sem 2
