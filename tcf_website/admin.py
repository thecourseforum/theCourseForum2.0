# pylint: disable=missing-class-docstring, wildcard-import

"""TCF Django Admin."""

from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Vote)


class SchoolAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class SubjectAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class DepartmentAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class SemesterAdmin(admin.ModelAdmin):
    ordering = ['-number']
    search_fields = ['season', 'year']


class CourseAdmin(admin.ModelAdmin):
    ordering = ['subject__mnemonic', 'number', 'title']
    search_fields = ['subject__mnemonic', 'number']


class InstructorAdmin(admin.ModelAdmin):
    ordering = ['last_name', 'first_name']
    search_fields = ['first_name', 'last_name']


class SectionAdmin(admin.ModelAdmin):
    search_fields = [
        'course__subject__mnemonic',
        'course__number',
        'course__title']
    autocomplete_fields = ['instructors']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('instructors')
        return qs


class CourseGradeAdmin(admin.ModelAdmin):
    ordering = ['subject', 'number', 'title']
    search_fields = ['subject', 'number']


class CourseInstructorGradeAdmin(admin.ModelAdmin):
    ordering = ['last_name', 'first_name']
    search_fields = ['first_name', 'last_name']


admin.site.register(Section, SectionAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(CourseGrade, CourseGradeAdmin)
admin.site.register(CourseInstructorGrade, CourseInstructorGradeAdmin)
