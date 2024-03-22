"""
This script downloads data from SIS API and converts it into
a usable CSV file. However, in its current state we have to
manually hardcode the year/season of the semester(s) we want to
download.

Potential todo: create a cron job that runs this script and
`load_semester` every now and then so we don't have to do this.
"""

# Classes intended stream finds each department, from there make a query to find each class in the department,
# however, this initial query is less detailed, so we would take this data to form queries for each class seperately
# using the course_nbr variable. Then this data is written to a csv.

import csv
import json
import os
import sys
from tqdm import tqdm
import backoff

# format -ClassNumber,Mnemonic,Number,Section,Type,Units,Instructor1,Days1,Room1,MeetingDates1,Instructor2,Days2,Room2,MeetingDates2,Instructor3,Days3,Room3,MeetingDates3,Instructor4,Days4,Room4,MeetingDates4,Title,Topic,Status,Enrollment,EnrollmentLimit,Waitlist,Description
# example call url
# -https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=UVA01&term=1242&class_nbr=16634&
import requests

# url to find all courses in department for a semester to update semester Replace 1228 with the appropriate term.
# The formula is “1” + [2 digit year] + [2 for Spring, 8 for Fall]. So, 1228 is Fall 2022.
# todo find out which is used for j term/summer probably 0,4, or 6?
# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=CS&page=1

# finds all departments in a term:
# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228


@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    max_tries=5,
)
def retrieve_semester_courses(sem_code):
    """
    input: semester using the formula  “1” + [2 digit year] + [2 for Spring, 8 for Fall]. So, 1228 is Fall 2022.
    output: list of dictionaries where each dictionary is all a course's information for the csv writing
    functionality: connects with sis API and looks at each class. It finds each course's course-number then passes it to compile_course_data
     which returns a dictionary of all of a course's information, which is added to a list containing the course info for all classes.
     This is done using a page by page approach where all the courses are analyzed one page at a time.
    """
    semester_url = (
        f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/"
        f"WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?"
        f"institution=UVA01&term={sem_code}&page="
    )

    all_classes = []
    page = 1
    while True:
        print(f"\nFetching page {page}...")
        page_url = semester_url + str(page)
        try:
            response = requests.get(page_url, timeout=300)
            page_data = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

        if not page_data:
            break

        for course in tqdm(page_data):
            class_data = compile_course_data(
                course["class_nbr"], sem_code
            )
            if class_data:
                all_classes.append(class_data)
        write_to_csv(all_classes)
        all_classes = []
        page += 1

    print("Data fetching complete.")


def compile_course_data(course_number, sem_code):
    """
    Compiles course data from SIS API response.

    :param course_number: The course number.
    :param sem_code: The semester code.
    :return: Dictionary containing course information.
    """
    url = (
        f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/"
        f"WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?"
        f"institution=UVA01&term={sem_code}&class_nbr={course_number}"
    )

    try:
        response = requests.get(url, timeout=300)
    except requests.exceptions.RequestException:
        return None

    data = json.loads(response.text)
    if not data:
        return None

    class_details = data["section_info"]["class_details"]
    meetings = {0: None, 1: None, 2: None, 3: None}

    for index, meeting in enumerate(data["section_info"]["meetings"]):
        if index > 3:
            break
        meetings[index] = meeting

    class_availability = data["section_info"]["class_availability"]

    course_dictionary = {
        "ClassNumber": course_number,
        "Mnemonic": class_details["subject"],
        "Number": class_details["catalog_nbr"],
        "Section": class_details["class_section"],
        "Type": {
            "LEC": "Lecture",
            "DIS": "Discussion",
            "LAB": "Laboratory",
        }.get(class_details["component"], class_details["component"]),
        "Units": class_details["units"][
            0 : class_details["units"].find("units") - 1
        ],
        "Instructor1": (
            ", ".join(
                instructor["name"]
                for instructor in meetings.get(0)["instructors"]
                if instructor["name"] != "-"
            )
            if meetings.get(0)
            else ""
        ),
        "Days1": (
            meetings.get(0)["meets"]
            if meetings.get(0)["meets"] != "-"
            else "TBA"
        ),
        "Room1": (
            meetings.get(0)["room"]
            if meetings.get(0)["room"] != "-"
            else "TBA"
        ),
        "MeetingDates1": (
            meetings.get(0)["date_range"] if meetings.get(0) else ""
        ),
        "Instructor2": (
            ", ".join(
                instructor["name"]
                for instructor in meetings.get(1)["instructors"]
                if instructor["name"] != "-"
            )
            if meetings.get(1)
            else ""
        ),
        "Days2": meetings.get(1)["meets"] if meetings.get(1) else "",
        "Room2": meetings.get(1)["room"] if meetings.get(1) else "",
        "MeetingDates2": (
            meetings.get(1)["date_range"] if meetings.get(1) else ""
        ),
        "Instructor3": (
            ", ".join(
                instructor["name"]
                for instructor in meetings.get(2)["instructors"]
                if instructor["name"] != "-"
            )
            if meetings.get(2)
            else ""
        ),
        "Days3": meetings.get(2)["meets"] if meetings.get(2) else "",
        "Room3": meetings.get(2)["room"] if meetings.get(2) else "",
        "MeetingDates3": (
            meetings.get(2)["date_range"] if meetings.get(2) else ""
        ),
        "Instructor4": (
            ", ".join(
                instructor["name"]
                for instructor in meetings.get(3)["instructors"]
                if instructor["name"] != "-"
            )
            if meetings.get(3)
            else ""
        ),
        "Days4": meetings.get(3)["meets"] if meetings.get(3) else "",
        "Room4": meetings.get(3)["room"] if meetings.get(3) else "",
        "MeetingDates4": (
            meetings.get(3)["date_range"] if meetings.get(3) else ""
        ),
        "Title": class_details["course_title"],
        "Topic": class_details["topic"],
        "Status": class_details["status"],
        "Enrollment": class_availability["enrollment_total"],
        "EnrollmentLimit": class_availability["class_capacity"],
        "Waitlist": class_availability["wait_list_total"],
        "Description": data["section_info"]["catalog_descr"][
            "crse_catalog_description"
        ]
        .replace("\n", " ")
        .replace("\r", " "),
    }
    return course_dictionary


def write_to_csv(course_list):
    """
    Writes course data to a CSV file.

    :param course_list: List of dictionaries containing course information.
    """
    print("Writing to CSV...")
    fieldnames = list(course_list[0].keys())
    with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for course in course_list:
            writer.writerow(course)


SEASON_NUMBERS = {"fall": 8, "summer": 6, "spring": 2, "january": 1}
COURSE_DATA_DIR = "sis_csv/"

arguments = sys.argv[1:]

if not arguments:
    sys.stdout.write(
        "No argument given. Give an argument in format: <year>_<season>"
    )
elif "--help" in arguments or "-h" in arguments:
    sys.stdout.write(
        "Fetches data from SIS API for the specified semester and saves it to a CSV file"
    )
elif not arguments[0]:
    sys.stdout.write(
        "No argument given. Give an argument in format: <year>_<season>"
    )
elif (
    len(elements:=arguments[0].split("_")) != 2
    or not elements[0].isdigit()
    or len(elements[0]) != 4
    or elements[1].lower() not in SEASON_NUMBERS
):
    sys.stdout.write(
        "Argument given in improper format. Give an argument in format: <year>_<season>"
    )
else:  # correct arguments
    year, season = arguments[0].split("_")
    season = season.lower()
    year_code = str(year)[-2:]
    sem_code = f"1{year_code}{SEASON_NUMBERS.get(season)}"  # 1 represents 21st century in querying
    sys.stdout.write(f"Fetching course data for {year} {season}...\n")
    filename = f"{year}_{season}.csv"
    csv_path = os.path.join(COURSE_DATA_DIR, filename)

    if os.path.exists(csv_path):
        os.remove(csv_path)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    retrieve_semester_courses(sem_code)

## test SIS data against Lous List data (remove function later)
# def compare_csv_files():
#     with open("SIS_2023_spring.csv", "r") as sis_file:
#         sis_reader = csv.reader(sis_file)
#         with open(
#             "tcf_website/management/commands/semester_data/csv/2023_spring.csv",
#             "r",
#         ) as lous_file:
#             local_reader = csv.reader(lous_file)
#             for sis_row, local_row in zip(sis_reader, local_reader):
#                 for sis_col, local_col in zip(sis_row, local_row):
#                     if sis_col != local_col:
#                         print("Course #:", sis_row[0])
#                         print("Discrepancy:")
#                         print("SIS: ", sis_col)
#                         print("Lou's: ", local_col)
#                         input("Enter to continue...\n")
#
#
# # compare_csv_files()
