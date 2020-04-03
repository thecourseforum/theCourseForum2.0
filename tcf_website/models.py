# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Courses(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    course_number = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    subdepartment_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title_changed = models.IntegerField(blank=True, null=True)
    last_taught_semester_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'courses'


class CoursesUsers(models.Model):
    course_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'courses_users'


class Departments(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    school_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'departments'


class DepartmentsSubdepartments(models.Model):
    department_id = models.IntegerField(blank=True, null=True)
    subdepartment_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'departments_subdepartments'


class Grades(models.Model):
    section_id = models.IntegerField(blank=True, null=True)
    semester_id = models.IntegerField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    count_a = models.IntegerField(blank=True, null=True)
    count_aminus = models.IntegerField(blank=True, null=True)
    count_bplus = models.IntegerField(blank=True, null=True)
    count_b = models.IntegerField(blank=True, null=True)
    count_bminus = models.IntegerField(blank=True, null=True)
    count_cplus = models.IntegerField(blank=True, null=True)
    count_c = models.IntegerField(blank=True, null=True)
    count_cminus = models.IntegerField(blank=True, null=True)
    count_dplus = models.IntegerField(blank=True, null=True)
    count_d = models.IntegerField(blank=True, null=True)
    count_dminus = models.IntegerField(blank=True, null=True)
    count_f = models.IntegerField(blank=True, null=True)
    count_drop = models.IntegerField(blank=True, null=True)
    count_withdraw = models.IntegerField(blank=True, null=True)
    count_other = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    count_aplus = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'grades'

class Majors(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'majors'

class Professors(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    preferred_name = models.CharField(max_length=255, blank=True, null=True)
    email_alias = models.CharField(max_length=255, blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    classification = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    department_code = models.TextField(blank=True, null=True)
    primary_email = models.TextField(blank=True, null=True)
    office_phone = models.TextField(blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    registered_email = models.TextField(blank=True, null=True)
    fax_phone = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    home_phone = models.TextField(blank=True, null=True)
    home_page = models.TextField(blank=True, null=True)
    mobile_phone = models.TextField(blank=True, null=True)
    professor_salary_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'professors'


class Reviews(models.Model):
    comment = models.TextField(blank=True, null=True)
    course_professor_id = models.IntegerField(blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    semester_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    professor_rating = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    enjoyability = models.IntegerField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    amount_reading = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    amount_writing = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    amount_group = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    amount_homework = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    only_tests = models.IntegerField(blank=True, null=True)
    recommend = models.IntegerField(blank=True, null=True)
    ta_name = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.IntegerField(blank=True, null=True)
    professor_id = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField()

    class Meta:
        db_table = 'reviews'


class Schedules(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    flagged = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'schedules'


class SchedulesSections(models.Model):
    schedule_id = models.IntegerField()
    section_id = models.IntegerField()

    class Meta:
        db_table = 'schedules_sections'


class SchemaMigrations(models.Model):
    version = models.CharField(max_length=255)

    class Meta:
        db_table = 'schema_migrations'


class Schools(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'schools'


class SectionProfessors(models.Model):
    section_id = models.IntegerField(blank=True, null=True)
    professor_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'section_professors'


class Sections(models.Model):
    sis_class_number = models.IntegerField(blank=True, null=True)
    section_number = models.IntegerField(blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    units = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    section_type = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.IntegerField(blank=True, null=True)
    semester_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sections'


class Semesters(models.Model):
    number = models.IntegerField(blank=True, null=True)
    season = models.CharField(max_length=255, blank=True, null=True)
    year = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'semesters'


class Settings(models.Model):
    var = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    target_id = models.IntegerField()
    target_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'settings'


class Stats(models.Model):
    course_id = models.IntegerField(blank=True, null=True)
    professor_id = models.IntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)  # This field type is a guess.
    difficulty = models.TextField(blank=True, null=True)  # This field type is a guess.
    gpa = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'stats'


class StudentMajors(models.Model):
    student_id = models.IntegerField(blank=True, null=True)
    major_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'student_majors'


class Students(models.Model):
    grad_year = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    user_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'students'


class Subdepartments(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    mnemonic = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'subdepartments'


class TextbookTransactions(models.Model):
    seller_id = models.IntegerField()
    buyer_id = models.IntegerField(blank=True, null=True)
    book_id = models.IntegerField()
    price = models.IntegerField()
    condition = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sold_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'textbook_transactions'


class Users(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    cellphone = models.CharField(max_length=255, blank=True, null=True)
    old_password = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    professor_id = models.IntegerField(blank=True, null=True)
    subscribed_to_email = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    encrypted_password = models.CharField(max_length=255)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    sign_in_count = models.IntegerField(blank=True, null=True)
    current_sign_in_at = models.DateTimeField(blank=True, null=True)
    last_sign_in_at = models.DateTimeField(blank=True, null=True)
    current_sign_in_ip = models.CharField(max_length=255, blank=True, null=True)
    last_sign_in_ip = models.CharField(max_length=255, blank=True, null=True)
    confirmation_token = models.CharField(max_length=255, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    unconfirmed_email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'users'


class Votes(models.Model):
    vote = models.IntegerField()
    voteable_id = models.IntegerField()
    voteable_type = models.CharField(max_length=255)
    voter_id = models.IntegerField(blank=True, null=True)
    voter_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'votes'
