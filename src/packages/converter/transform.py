from re import search

from django.core.files.uploadedfile import UploadedFile
from icalendar import Calendar
from pandas import DataFrame, read_excel

from .calendar import create_ical
from .data import convert_all


def import_data(file: UploadedFile | DataFrame) -> DataFrame:
    # TODO: !!! REFACTOR
    # TODO: make usable when file is a DataFrame
    """ Cleans the schedule data of a UBC schedule

    Args:
        file (UploadedFile): A file upload of a UBC workday schedule
        file (Dataframe): A DataFrame obtained by read_excel from pandas
                          of a UBC workday schedule

    Returns:
        A Dataframe of the schedeule content of the uploaded UBC workday
    schedule
    """

    start = _find_start(file)
    end = _find_end(file)

    return read_excel(file, skiprows=start, skipfooter=end)


def _find_start(file: UploadedFile) -> int:
    """
    Inputs:
    - file: a file upload of a UBC workday class schedule

    Returns:
    - an int of the index of the begining row of (the column names)
    the schedule data

    """

    data = read_excel(file, header=None)

    def _get_row_with_header() -> DataFrame:
        """
        Returns dataframe of row(s) in data that match the header row,
        keeping the same index values as data
        """
        header = (
            (data[0].isna())
            & (data[1] == "Course Listing")
            & (data[2] == "Credits")
            & (data[3] == "Grading Basis")
            & (data[4] == "Section")
            & (data[5] == "Instructional Format")
            & (data[6] == "Delivery Mode")
            & (data[7] == "Meeting Patterns")
            & (data[8] == "Registration Status")
            & (data[9] == "Instructor")
            & (data[10] == "Start Date")
            & (data[11] == "End Date")
        )
        return data[header]

    def _get_index_of_header() -> int:
        """
        Returns the index of the first row in data that contains all the
        column names
        """
        return _get_row_with_header().index[0]

    return _get_index_of_header()


def _find_end(file: UploadedFile) -> int:
    """
    Inputs:
    - file: a file upload of a UBC workday class schedule

    Returns:
    - the index of the ending row of the schedule data
    (the last enrolled course)

    """

    start = _find_start(file)
    data = read_excel(file, skiprows=start + 1, header=None)

    pattern = "\w+ \w+ \(\d{8}\)"

    index = 0
    for val in data[0]:
        if search(pattern, val) is None:
            return len(data[0]) - index
        else:
            index += 1
    else:
        return 0


def convert_file(file: UploadedFile | DataFrame) -> Calendar:
    data = import_data(file)

    converted = convert_all(data)
    data_dict = converted.to_dict(orient="records")

    return create_ical(data_dict)
