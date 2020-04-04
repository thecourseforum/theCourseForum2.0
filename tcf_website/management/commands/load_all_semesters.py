import os
import re

from tqdm import tqdm
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tcf_website.models import *



class Command(BaseCommand):
    help = 'Imports data from lous list csv\'s into default database'
    
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output',
        )

    def handle(self, *args, **options):

        self.verbose = options['verbose']

        self.UNKNOWN_SCHOOL, _ = School.objects.get_or_create(name='UNKNOWN')
        self.UNKNOWN_DEPT, _ = Department.objects.get_or_create(name='UNKNOWN', school = self.UNKNOWN_SCHOOL)
        self.STAFF, _ = Instructor.objects.get_or_create(last_name='Staff')

        self.data_dir = 'tcf_website/management/commands/semester_data/csv/'

        for file in os.listdir(self.data_dir):
            self.load_semester_file(file)
    
    def clean(self, df):
        return df.dropna(subset=['Mnemonic', 'ClassNumber', 'Number', 'Section'])
    
    def load_semester_file(self, file):
        year, semester = file.split('.')[0].split('_')
        year = int(year)
        season = semester.upper()

        print(year, season)

        df = self.clean(pd.read_csv(os.path.join(self.data_dir, file)))

        print(f"{df.size} sections")

        semester = self.load_semester(year, season)

        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            # print(row)
            self.load_section_row(semester, row)
            # break
    
    def load_semester(self, year, season):
        year_code = str(year)[-2:]
        season_code = {
            'FALL': 8,
            'SUMMER': 6,
            'SPRING': 2,
            'JANUARY': 1
        }[season]
        semester_code = f"1{year_code}{season_code}"

        sem, created = Semester.objects.get_or_create(
            year = year,
            season = season,
            number = semester_code,
        )

        if self.verbose:
            if created:
                print(f"Created {sem}")
            else:
                print(f"Retrieved {sem}")
            
        return sem
    
    def load_section_row(self, semester, row):
        # instructor_names = [row[column] for column in ['Instructor1', 'Instructor1', 'Instructor1', 'Instructor1']]
        # print(row)
        # print(row.index)
        # print()

        mnemonic = row['Mnemonic'] # may NOT be missing
        sis_number = row['ClassNumber'] # may NOT be missing
        # strip out non-numeric characters.
        course_number = re.sub('[^0-9]','', row['Number']) # may NOT be missing
        section_number = row['Section'] # may NOT be missing
        
        units = row['Units'] # may be empty/nan
        title = row['Title'] # may be empty/nan
        topic = row['Topic'] # may be empty/nan
        description = row['Description'] # may be empty/nan
        section_type = row['Type'] # may be empty/nan

        # may include staff, may be empty
        instructor_names = row[['Instructor1', 'Instructor2', 'Instructor3', 'Instructor4']].dropna().array

        sd = self.load_subdepartment(mnemonic)
        course = self.load_course(title, description, semester, sd, course_number)
        instructors = self.load_instructors(instructor_names)
        section = self.load_section(sis_number, instructors, semester, course, topic, units, section_type)
    
    def load_subdepartment(self, mnemonic):

        try:
            sd = Subdepartment.objects.get(
                mnemonic = mnemonic,
            )
            if self.verbose:
                print(f"Retrieved {sd}")
        except ObjectDoesNotExist: # no SD
            sd = Subdepartment(mnemonic=mnemonic, department=self.UNKNOWN_DEPT)
            sd.save()
            if self.verbose:
                print(f"Created {sd}")
        return sd

    # TODO: how to handle special topics courses?
    # topic: section topic
    # description: course description!
    def load_course(self, title, description, semester, subdepartment, number):
        
        params = {}
        fields = {'title', 'description', 'subdepartment', 'number'}
        for k, v in locals().items():
            if k in fields and not pd.isnull(v):
                params[k] = v

        try:
            course = Course.objects.get(**params)
            if self.verbose:
                print(f"Retrieved {course}")
        except ObjectDoesNotExist:
            course = Course(**params)
            course.semester_last_taught = semester
            course.save()
            if self.verbose:
                print(f"Created {course}")
        except MultipleObjectsReturned as e:
            # multiple returner when there should be just one.
            print("Multiple courses returned for ")
            print(params)
            raise e

        if semester.is_after(course.semester_last_taught):
            course.semester_last_taught = semester
        
        return course
    
    def load_instructors(self, instructor_names):
        instructors = set()
        for name in instructor_names:
            if name == 'Staff':
                instructors.add(self.STAFF)
            else:
                names = name.split()
                first, last = names[0], names[-1]

                instructor, created = Instructor.objects.get_or_create(
                    first_name = first,
                    last_name = last,
                )
                if self.verbose:
                    if created:
                        print(f"Created {instructor}")
                    else:
                        print(f"Retrieved {instructor}")
                instructors.add(instructor)
        return instructors

    def load_section(self, sis_section_number, instructors, semester, course, topic, units, section_type):
        
        params = {}
        fields = {'sis_section_number', 'semester', 'course', 'topic', 'units', 'section_type'}
        for k, v in locals().items():
            if k in fields and not pd.isnull(v):
                params[k] = v

        # print(locals())
        section, created = Section.objects.get_or_create(
            **params
        )

        for instructor in instructors:
            section.instructors.add(instructor)

        if self.verbose:
            if created:
                print(f"Created {section}")
            else:
                print(f"Retrieved {section}")
        
        return section