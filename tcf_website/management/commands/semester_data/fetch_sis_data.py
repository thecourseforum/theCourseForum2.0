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

# format -ClassNumber,Mnemonic,Number,Section,Type,Units,Instructor1,Days1,Room1,MeetingDates1,Instructor2,Days2,Room2,MeetingDates2,Instructor3,Days3,Room3,MeetingDates3,Instructor4,Days4,Room4,MeetingDates4,Title,Topic,Status,Enrollment,EnrollmentLimit,Waitlist,Description
# example call url
# -https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=UVA01&term=1242&class_nbr=16634&
import requests
import json
import csv

# url to find all courses in department for a semester to update semester Replace 1228 with the appropriate term.
# The formula is “1” + [2 digit year] + [2 for Spring, 8 for Fall]. So, 1228 is Fall 2022.
# todo find out which is used for j term/summer probably 0,4, or 6?
# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=CS&page=1

# finds all departments in a term:
# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228


def retrieve_semester_courses(semester):  # very slow
    """
    input: semester using the formula  “1” + [2 digit year] + [2 for Spring, 8 for Fall]. So, 1228 is Fall 2022.
    output: list of dictionaries where each dictionary is all a course's information for the csv writing
    functionality: connects with sis API and looks at each class. It finds each course's course-number then passes it to compile_course_data
     which returns a dictionary of all of a course's information, which is added to a list containing the course info for all classes.
     This is done using a page by page approach where all the courses are analyzed one page at a time."""
    semester_url = (
        'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.' +
        'FieldFormula.IScript_ClassSearch?institution=UVA01&term=' +
        semester +
        '&page=')
    all_classes = []
    page = 1  # Page is initially 1
    while page==1:  # loads the first 100 courses (page 1) # Loops through every page and extracts classes until it runs out of pages when the while breaks
        page_url = semester_url + str(page)
        try:
            apiResponse = requests.get(page_url)
            page_data = json.loads(apiResponse.text)
            if not page_data:  # checks to see if there is no data for that page which means that all
                # data has been extracted from previous pages so the loop breaks
                break
        except Exception as e:
            print(e)
            break
        for course in page_data:  # loops through every course on the page and calls compile_course_data and adds output to list
            # calls function to create dict of class info
            class_data = compile_course_data(course['class_nbr'], semester)
            if not class_data:
                continue
            all_classes.append(class_data)  # adds dict to list of all classes
        page += 1  # Incrementing page count so next query will be on next page
    return all_classes


def compile_course_data(course_number, semester):
    """
        input: course number, semester
        output: course dictionaries to be used for file writing
        functionality: request and organize course data in dictionaries to be able to write to a csv file.
    """
    url = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassDetails?institution=UVA01&term={semester}&class_nbr={course_number}"

    try:
        apiResponse = requests.get(url)
        data = json.loads(apiResponse.text)
        if data == []:
            return None
    except Exception as e:
        print(e)
        return None

    class_details = data["section_info"]["class_details"]
    meetings = [None, None, None, None]
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
        # For Type, Parser needs to be updated to use abbriveation instead of full
        # word (LEC instead of Lecture)
        "Type": {
            "LEC": "Lecture",
            "DIS": "Discussion",
            "LAB": "Laboratory"
        }.get(class_details["component"], class_details["component"]),
        "Units": class_details["units"][0:class_details["units"].find("u") - 1],
        "Instructor1": ", ".join(instructor["name"] for instructor in meetings[0]["instructors"] if instructor["name"] != "-") if meetings[0] else "",
        "Days1": meetings[0]["meets"] if meetings[0]["meets"] != "-" else "TBA",
        "Room1": meetings[0]["room"] if meetings[0]["room"] != "-" else "TBA",
        "MeetingDates1": meetings[0]["start_date"] + " - " + meetings[0]["end_date"] if meetings[0] else "",
        "Instructor2": ", ".join(instructor["name"] for instructor in meetings[1]["instructors"]) if meetings[1] else "",
        "Days2": meetings[1]["meets"] if meetings[1] else "",
        "Room2": meetings[1]["room"] if meetings[1] else "",
        "MeetingDates2": meetings[1]["start_date"] + " - " + meetings[1]["end_date"] if meetings[1] else "",
        "Instructor3": ", ".join(instructor["name"] for instructor in meetings[2]["instructors"]) if meetings[2] else "",
        "Days3": meetings[2]["meets"] if meetings[2] else "",
        "Room3": meetings[2]["room"] if meetings[2] else "",
        "MeetingDates3": meetings[2]["start_date"] + " - " + meetings[2]["end_date"] if meetings[2] else "",
        "Instructor4": ", ".join(instructor["name"] for instructor in meetings[3]["instructors"]) if meetings[3] else "",
        "Days4": meetings[3]["meets"] if meetings[3] else "",
        "Room4": meetings[3]["room"] if meetings[3] else "",
        "MeetingDates4": meetings[3]["start_date"] + " - " + meetings[3]["end_date"] if meetings[3] else "",
        "Title": class_details["course_title"],
        "Topic": class_details["topic"],
        "Status": class_details["status"],
        "Enrollment": class_availability["enrollment_total"],
        "EnrollmentLimit": class_availability["class_capacity"],
        "Waitlist": class_availability["wait_list_total"],
        "Description": data["section_info"]["catalog_descr"]["crse_catalog_description"]
    }
    return course_dictionary


def write_csv(courseList, filename):
    fieldnames = list(courseList[0].keys())
    csv_filename = filename + ".csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for course in courseList:
            writer.writerow(course)


write_csv(retrieve_semester_courses("1232"), "SIS_2023_spring")

# test SIS data against Lous List data (remove function later)


def compare_csv_files():
    with open('SIS_2023_spring.csv', 'r') as sis_file:
        sis_reader = csv.reader(sis_file)
        with open('tcf_website/management/commands/semester_data/csv/2023_spring.csv', 'r') as lous_file:
            local_reader = csv.reader(lous_file)
            for sis_row, local_row in zip(sis_reader, local_reader):
                if sis_row != local_row:
                    print("Discrepancy:")
                    print("SIS row: ", sis_row)
                    print("Local row: ", local_row)
                    input("Enter to continue...\n")


compare_csv_files()