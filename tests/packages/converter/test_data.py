import sys

sys.path.append("./")
from copy import deepcopy

from pandas import DataFrame, read_excel

from src.packages.converter.data import (
    convert_all,
    convert_cols,
    split_course,
    split_meeting_patterns,
)

dataframe = read_excel("data/View_My_Courses_1.xlsx", skiprows=2)
data = dataframe.astype(str).to_dict(orient="records")

### split_meeting_patterns() tests


def test_split_meeting_patterns_2mp_2long():
    assert split_meeting_patterns(
        [
            {
                "Meeting Patterns": "meeting - pattern - 1\n\nmeeting - pattern - 2"
            },
            {
                "Meeting Patterns": "meeting - pattern - 3\n\nmeeting - pattern - 4"
            },
        ]
    ) == [
        {"Meeting Patterns": "meeting - pattern - 1"},
        {"Meeting Patterns": "meeting - pattern - 2"},
        {"Meeting Patterns": "meeting - pattern - 3"},
        {"Meeting Patterns": "meeting - pattern - 4"},
    ]


def test_split_meeting_patterns_1mp_1long():
    assert split_meeting_patterns(data[4:5]) == data[4:5]


b = deepcopy(data[5:6]) + deepcopy(data[5:6])
b[0][
    "Meeting Patterns"
] = "2025-01-06 - 2025-02-12 | Mon Wed | 8:00 a.m. - 9:30 a.m. | ESB-Floor 1-Room 1012"
b[1][
    "Meeting Patterns"
] = "2025-02-24 - 2025-04-07 | Mon Wed | 8:00 a.m. - 9:30 a.m. | ESB-Floor 1-Room 1012"


def test_split_meeting_patterns_2mp_1long():
    assert split_meeting_patterns(data[5:6]) == b


### split_course() tests


def test_split_course_1_meeting_pattern():

    assert split_course({"Meeting Patterns": "m - p - 1"}) == [
        {"Meeting Patterns": "m - p - 1"}
    ]


def test_split_course_2_meeting_patterns():

    assert split_course({"Meeting Patterns": "m - p - 1\n\nm - p - 2"}) == [
        {"Meeting Patterns": "m - p - 1"},
        {"Meeting Patterns": "m - p - 2"},
    ]


### split_course() tests


def test_split_course_1mp():
    test_input = {
        "": "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
        "Course Listing": "STAT_V 200 - Elementary Statistics for Applications",
        "Credits": "3",
        "Grading Basis": "Graded",
        "Section": "STAT_V 200-103 - Elementary Statistics for Applications",
        "Instructional Format": "Lecture",
        "Delivery Mode": "In Person Learning",
        "Meeting Patterns": "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
        "Registration Status": "Registered",
        "Instructor": "Rodolfo Lourenzutti",
        "Start Date": "2024-09-03",
        "End Date": "2024-12-06",
    }

    expected_output = [
        {
            "": "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
            "Course Listing": "STAT_V 200 - Elementary Statistics for Applications",
            "Credits": "3",
            "Grading Basis": "Graded",
            "Section": "STAT_V 200-103 - Elementary Statistics for Applications",
            "Instructional Format": "Lecture",
            "Delivery Mode": "In Person Learning",
            "Meeting Patterns": "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
            "Registration Status": "Registered",
            "Instructor": "Rodolfo Lourenzutti",
            "Start Date": "2024-09-03",
            "End Date": "2024-12-06",
        }
    ]

    assert split_course(test_input) == expected_output


def test_split_course_2mp():

    test_input = {
        "": "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
        "Course Listing": "STAT_V 200 - Elementary Statistics for Applications",
        "Credits": "3",
        "Grading Basis": "Graded",
        "Section": "STAT_V 200-103 - Elementary Statistics for Applications",
        "Instructional Format": "Lecture",
        "Delivery Mode": "In Person Learning",
        "Meeting Patterns": "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100\n\n2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
        "Registration Status": "Registered",
        "Instructor": "Rodolfo Lourenzutti",
        "Start Date": "2024-09-03",
        "End Date": "2024-12-06",
    }

    expected_output = [
        {
            "": "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
            "Course Listing": "STAT_V 200 - Elementary Statistics for Applications",
            "Credits": "3",
            "Grading Basis": "Graded",
            "Section": "STAT_V 200-103 - Elementary Statistics for Applications",
            "Instructional Format": "Lecture",
            "Delivery Mode": "In Person Learning",
            "Meeting Patterns": "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
            "Registration Status": "Registered",
            "Instructor": "Rodolfo Lourenzutti",
            "Start Date": "2024-09-03",
            "End Date": "2024-12-06",
        },
        {
            "": "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
            "Course Listing": "STAT_V 200 - Elementary Statistics for Applications",
            "Credits": "3",
            "Grading Basis": "Graded",
            "Section": "STAT_V 200-103 - Elementary Statistics for Applications",
            "Instructional Format": "Lecture",
            "Delivery Mode": "In Person Learning",
            "Meeting Patterns": "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
            "Registration Status": "Registered",
            "Instructor": "Rodolfo Lourenzutti",
            "Start Date": "2024-09-03",
            "End Date": "2024-12-06",
        },
    ]

    assert split_course(test_input) == expected_output


### convert_cols() tests
# TODO: test convert_cols()


def test_convert_cols_1long():
    test_input = {
        "Section": ["STAT_V 200-103 - Elementary Statistics for Applications"],
        "Meeting Patterns": [
            "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100"
        ],
    }

    expected_output = {
        "Section": ["STAT 200 103"],
        "Meeting Patterns": [
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            }
        ],
    }

    test_input = DataFrame(test_input)
    convert_cols(test_input)
    expected_output = DataFrame(expected_output)

    assert expected_output.equals(test_input) == True


def test_convert_cols_2long():  # TODO:
    test_input = {
        "Section": [
            "STAT_V 200-103 - Elementary Statistics for Applications",
            "ANTH_V 100-A_003 - Introduction to Cultural Anthropology (A)",
        ],
        "Meeting Patterns": [
            "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
            "2024-09-03 - 2024-12-04 | Mon Wed | 12:00 p.m. - 1:00 p.m. | MATH-Floor 1-Room 100",
        ],
    }

    expected_output = {
        "Section": ["STAT 200 103", "ANTH 100 A_003"],
        "Meeting Patterns": [
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            },
            {
                "start_date": "20240903",
                "end_date": "20241204",
                "days": ["MO", "WE"],
                "start_time": "120000",
                "end_time": "130000",
                "room": "MATH Floor 1 Room 100",
            },
        ],
    }

    test_input = DataFrame(test_input)
    convert_cols(test_input)
    expected_output = DataFrame(expected_output)

    assert expected_output.equals(test_input)


### convert_all() tests


# test 1 long 1 meeting pattern
def test_convert_all_1mp():
    test_input = {
        "": [
            "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)"
        ],
        "Course Listing": [
            "STAT_V 200 - Elementary Statistics for Applications"
        ],
        "Credits": ["3"],
        "Grading Basis": ["Graded"],
        "Section": ["STAT_V 200-103 - Elementary Statistics for Applications"],
        "Instructional Format": ["Lecture"],
        "Delivery Mode": ["In Person Learning"],
        "Meeting Patterns": [
            "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100"
        ],
        "Registration Status": ["Registered"],
        "Instructor": ["Rodolfo Lourenzutti"],
        "Start Date": ["2024-09-03"],
        "End Date": ["2024-12-06"],
    }
    expected_ouput = {
        "Section": ["STAT 200 103"],
        "Meeting Patterns": [
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            }
        ],
    }

    test_input = DataFrame(test_input)
    expected_ouput = DataFrame(expected_ouput)

    print(test_input)
    print(expected_ouput)

    assert expected_ouput.equals(convert_all(test_input)) == True


# test 1 long 2 meeting patterns
def test_convert_all_2mp():
    test_input = {
        "": [
            "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)"
        ],
        "Course Listing": [
            "STAT_V 200 - Elementary Statistics for Applications"
        ],
        "Credits": ["3"],
        "Grading Basis": ["Graded"],
        "Section": ["STAT_V 200-103 - Elementary Statistics for Applications"],
        "Instructional Format": ["Lecture"],
        "Delivery Mode": ["In Person Learning"],
        "Meeting Patterns": [
            "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100\n\n2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100"
        ],
        "Registration Status": ["Registered"],
        "Instructor": ["Rodolfo Lourenzutti"],
        "Start Date": ["2024-09-03"],
        "End Date": ["2024-12-06"],
    }
    expected_ouput = {
        "Section": ["STAT 200 103", "STAT 200 103"],
        "Meeting Patterns": [
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            },
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            },
        ],
    }

    test_input = DataFrame(test_input)
    expected_ouput = DataFrame(expected_ouput)

    assert expected_ouput.equals(convert_all(test_input)) == True


# test 2 long, second item has 2 meeting patterns
def test_convert_all_2long_2mp():
    test_input = {
        "": [
            "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - STAT_V 200 - Elementary Statistics for Applications - 2024-25 Winter Term 1 (UBC-V)",
            "Andrei Doroteo (41101338) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - ANTH_V 100 - Introduction to Cultural Anthropology - 2024-25 Winter Term 1 (UBC-V)",
        ],
        "Course Listing": [
            "STAT_V 200 - Elementary Statistics for Applications",
            "ANTH_V 100 - Introduction to Cultural Anthropology",
        ],
        "Credits": ["3", "3"],
        "Grading Basis": ["Graded", "Graded"],
        "Section": [
            "STAT_V 200-103 - Elementary Statistics for Applications",
            "ANTH_V 100-A_003 - Introduction to Cultural Anthropology (A)",
        ],
        "Instructional Format": ["Lecture", "Lecture"],
        "Delivery Mode": ["In Person Learning", "In Person Learning"],
        "Meeting Patterns": [
            "2024-09-03 - 2024-12-06 | Mon Wed Fri | 2:00 p.m. - 3:00 p.m. | WESB-Floor 1-Room 100",
            "2024-09-03 - 2024-12-04 | Mon Wed | 12:00 p.m. - 1:00 p.m. | MATH-Floor 1-Room 100\n\n2024-09-03 - 2024-12-04 | Mon Wed | 12:00 p.m. - 1:00 p.m. | MATH-Floor 1-Room 100",
        ],
        "Registration Status": ["Registered", "Registered"],
        "Instructor": ["Rodolfo Lourenzutti", "Charles Menzies"],
        "Start Date": ["2024-09-03", "2024-09-03"],
        "End Date": ["2024-12-06", "2024-12-06"],
    }
    expected_ouput = {
        "Section": ["STAT 200 103", "ANTH 100 A_003", "ANTH 100 A_003"],
        "Meeting Patterns": [
            {
                "start_date": "20240903",
                "end_date": "20241206",
                "days": ["MO", "WE", "FR"],
                "start_time": "140000",
                "end_time": "150000",
                "room": "WESB Floor 1 Room 100",
            },
            {
                "start_date": "20240903",
                "end_date": "20241204",
                "days": ["MO", "WE"],
                "start_time": "120000",
                "end_time": "130000",
                "room": "MATH Floor 1 Room 100",
            },
            {
                "start_date": "20240903",
                "end_date": "20241204",
                "days": ["MO", "WE"],
                "start_time": "120000",
                "end_time": "130000",
                "room": "MATH Floor 1 Room 100",
            },
        ],
    }

    test_input = DataFrame(test_input)
    expected_ouput = DataFrame(expected_ouput)

    assert expected_ouput.equals(convert_all(test_input))


# tests the case where a schedule has 2 courses and one course
# has no room assignment
def test_convert_all_2long_2mp_no_room():
    test_input = {
        "": [
            "Sample Student (00000000) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - ARCL_V 103 - Introduction to Archaeology:  Past perspectives and Future Promise - 2024-25 Winter Term 2 (UBC-V)",
            "Sample Student (00000000) - Faculty of Science (Vancouver)/Undergraduate (B.Sc.) - 2024-06-21 - Active - CHEM_V 213 - Organic Chemistry - 2024-25 Winter Term 2 (UBC-V)",
        ],
        "Course Listing": [
            "ARCL_V 103 - Introduction to Archaeology:  Past perspectives and Future Promise",
            "CHEM_V 213 - Organic Chemistry",
        ],
        "Credits": ["3", "3"],
        "Grading Basis": ["Graded", "Graded"],
        "Section": [
            "ARCL_V 103-D1C - Introduction to Archaeology:  Past perspectives and Future Promise",
            "CHEM_V 213-201 - Organic Chemistry",
        ],
        "Instructional Format": ["Discussion", "Lecture"],
        "Delivery Mode": ["In Person Learning", "In Person Learning"],
        "Meeting Patterns": [
            "2025-01-10 - 2025-02-14 | Fri | 11:00 a.m. - 12:00 p.m. |\n\n2025-02-28 - 2025-04-04 | Fri | 11:00 a.m. - 12:00 p.m. |",
            "2025-01-06 - 2025-02-14 | Mon Wed Fri | 1:00 p.m. - 2:00 p.m. | WESB-Floor 1-Room 100\n\n2025-02-24 - 2025-04-07 | Mon Wed Fri | 1:00 p.m. - 2:00 p.m. | WESB-Floor 1-Room 100",
        ],
        "Registration Status": ["Registered", "Registered"],
        "Instructor": ["Samantha Walker", "Jason Hein"],
        "Start Date": ["1/7/2025", "1/6/2025"],
        "End Date": ["4/8/2025", "4/7/2025"],
    }
    expected_ouput = {
        "Section": [
            "ARCL 103 D1C",
            "ARCL 103 D1C",
            "CHEM 213 201",
            "CHEM 213 201",
        ],
        "Meeting Patterns": [
            {
                "start_date": "20250110",
                "end_date": "20250214",
                "days": ["FR"],
                "start_time": "110000",
                "end_time": "120000",
                "room": "",
            },
            {
                "start_date": "20250228",
                "end_date": "20250404",
                "days": ["FR"],
                "start_time": "110000",
                "end_time": "120000",
                "room": "",
            },
            {
                "start_date": "20250106",
                "end_date": "20250214",
                "days": ["MO", "WE", "FR"],
                "start_time": "130000",
                "end_time": "140000",
                "room": "WESB Floor 1 Room 100",
            },
            {
                "start_date": "20250224",
                "end_date": "20250407",
                "days": ["MO", "WE", "FR"],
                "start_time": "130000",
                "end_time": "140000",
                "room": "WESB Floor 1 Room 100",
            },
        ],
    }

    test_input = DataFrame(test_input)
    expected_ouput = DataFrame(expected_ouput)

    assert expected_ouput.equals(convert_all(test_input))
