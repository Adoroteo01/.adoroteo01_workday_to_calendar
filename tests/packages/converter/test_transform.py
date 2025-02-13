import pytest
from pandas import read_excel

from src.packages.converter.transform import (
    _find_end,
    _find_start,
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
def data_path(test_data):
    """returns the path of a schedule in test_data"""
    return test_data[0]


def test_import_data(data_path, expected):
    assert import_data(data_path).equals(expected)


def test_find_start():
    assert _find_start("data/View_My_Courses_1.xlsx") == 2
    assert _find_start("data/View_My_Courses_2.xlsx") == 5


def test_find_end():
    assert _find_end("data/View_My_Courses_1.xlsx") == 0
    assert _find_end("data/View_My_Courses_2.xlsx") == 7


# TODO: !!! add tests for when users download during sem 1 versus sem 2
