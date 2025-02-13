import pytest
from pandas import read_excel

from src.packages.converter import convert_file
from src.packages.converter.ubcschedule import UBCSchedule


def get_paths():
    with open(
        "tests/packages/converter/test_data/schedule_paths.txt",
        "r",
    ) as file:
        paths = []
        for line in file:
            paths.append(line.strip("\n"))
        return paths


@pytest.fixture(params=get_paths())
def test_data_path(request):

    return request.param


@pytest.fixture
def schedule(test_data_path):
    data = read_excel(test_data_path)

    return UBCSchedule(data)


@pytest.fixture
def data(test_data_path):
    return read_excel(test_data_path)


def test_constructor(schedule, data):

    assert data.equals(schedule.data)
    assert schedule.calendar is None


def test_update_calendar(schedule, data):

    schedule.update_calendar()
    expected = convert_file(data)

    assert expected.equals(schedule.calendar)
