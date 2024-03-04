"""View pertaining to schedule creation/viewing."""
import json

from django import forms
# from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin  # For class-based views
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from django.db.models import Prefetch

from .browse import load_secs_helper
from ..models import Schedule, User, Course, Semester, ScheduledCourse, Instructor, Section

# pylint: disable=line-too-long
# pylint: disable=no-else-return
# pylint: disable=consider-using-generator


class ScheduleForm(forms.ModelForm):
    '''
    Django form for interacting with a schedule
    '''
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Schedule
        fields = [
            'name', 'user_id'
        ]


class SectionForm(forms.ModelForm):
    '''
    Django form for adding a course to a schedule
    '''

    class Meta:
        model = ScheduledCourse
        fields = [
            'schedule', 'section', 'instructor', 'time'
        ]


@login_required
def get_schedule(schedule):
    ret = [0]*4
    ret[0] = schedule.get_scheduled_courses()
    # if a course doesn't have any units, just default to three
    ret[1] = sum([int(course.section.units) if int(
        course.section.units) != 0 else 3 for course in ret[0]])
    ret[2] = schedule.average_rating_for_schedule()
    ret[3] = schedule.average_schedule_difficulty()

    return ret


@login_required
def schedule_data_helper(request):
    '''
    this helper method is for getting schedule data for a request.
    '''

    schedules = Schedule.objects.prefetch_related(
        Prefetch(
            'scheduledcourse_set',
            queryset=ScheduledCourse.objects.select_related('section', 'instructor')
        )
    )
    courses_context = {}  # contains the joined table for Schedule and ScheduledCourse models
    ratings_context = {}  # contains aggregated ratings for schedules, using the model's method
    difficulty_context = {}  # contains aggregated difficulty of schedules, using the model's method
    credits_context = {}  # contains the total credits of schedules, calculated in this view

    # iterate over the schedules for this request in order to set up the context
    # this could also be optimized for the database by combining these queries
    for s in schedules:
        s_data = get_schedule(s)
        courses_context[s.id] = s_data[0]
        # if a course doesn't have any units, just default to three
        credits_context[s.id] = s_data[1]
        ratings_context[s.id] = s_data[2]
        difficulty_context[s.id] = s_data[3]

    ret = {"schedules": schedules,
           "courses": courses_context,
           "ratings": ratings_context,
           "difficulty": difficulty_context,
           "credits": credits_context}

    return ret


def view_schedules(request):
    '''
    get all schedules, and the related courses, for a given user
    '''
    schedule_context = schedule_data_helper(request)

    # add an empty schedule form into the context
    # to be used in the create_schedule_modal
    form = ScheduleForm()
    schedule_context['form'] = form

    return render(request,
                  'schedule/user_schedules.html',
                  schedule_context)


def view_schedules_modal(request, mode):
    '''
    get all schedules and display in the modal.

    the "mode" parameter in the url specfies which modal to render
    '''
    # NOTE: as of now, this endpoint is used as a means to load modal content
    # and not the modal itself

    schedule_context = schedule_data_helper(request)
    if mode == "add_course":
        # add necessary context variables for the select_schedule_modal template
        schedule_context['profile'] = True
        schedule_context['select'] = True
        schedule_context['mode'] = mode  # pass back the mode used for the request
        schedule_context['url_param'] = 'schedule'

        return render(request,
                      'schedule/schedules.html',
                      schedule_context)
    elif mode == "edit_schedule":
        # this mode is for loading schedules into the edit_schedule_modal template
        schedule_context['select'] = True
        schedule_context['url_param'] = 'schedule'
        schedule_context['mode'] = mode  # pass back the mode used for the request

        return render(request,
                      'schedule/schedules.html',
                      schedule_context)
    else:
        # redirect if there is no mode parameter
        # NOTE: there might be a better way to handle this error
        messages.error(request, "Missing or invalid mode parameter from query string")
        return redirect('schedule')


@login_required
def new_schedule(request):
    '''
    Take the user to the new schedule page
    '''
    if request.method == 'POST':
        # Handle saving the schedule
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            user_id = form.cleaned_data['user_id']  # get the user's primary key
            schedule.user = User.objects.get(id=user_id)
            if user_id == "" or schedule.user is None:
                messages.error(request, "There was an error")
                return render(request, 'schedule/user_schedules.html', {"form": form})
            schedule.save()
            messages.success(request, "Successfully created schedule!")
            return redirect('schedule')
    else:
        # if schedule isn't getting saved, then don't do anything
        # for part two of the this project, load the actual course builder page
        form = ScheduleForm()
    return render(request, 'schedule/schedule_builder.html', {"form": form})


@login_required
def delete_schedule(request):
    '''
    Delete a schedule or multiple schedules
    '''
    # we use POST since forms don't support the DELETE method
    if request.method == 'POST':
        # Retrieve IDs from POST data
        schedule_ids = request.POST.getlist('selected_schedules')
        schedule_count = len(schedule_ids)

        # Perform bulk delete
        deleted_count, _ = Schedule.objects.filter(id__in=schedule_ids).delete()
        if deleted_count == 0:
            messages.error(request, "No schedules were deleted.")
        else:
            messages.success(
                request,
                f"Successfully deleted {schedule_count} schedules and {deleted_count - schedule_count} courses")
    return redirect('schedule')


@login_required
def edit_schedule(request):
    '''
    Edit a schedule based on a selected schedule, and the changes passed in
    '''
    ret = {}
    if request.method == 'GET':
        ret['mode'] = 'edit'
        return JsonResponse(ret)

    return redirect('schedule')


@login_required
def modal_load_sections(request):
    '''
    Load the instructors and section times for a course, and the schedule, when adding to schedule from the modal
    '''

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    course_id = body['course_id']
    schedule_id = body['schedule_id']

    # get the course based off passed in course_id
    course = Course.objects.get(pk=course_id)
    latest_semester = Semester.latest()

    data = {}
    instructors = load_secs_helper(
        course, latest_semester).filter(
        semester_last_taught=latest_semester.id)

    for i in instructors:
        temp = {}
        data[i.id] = temp

        # decode the string in section_details and take skip strings without a time or section_id
        encoded_sections = [x.split(' /% ') for x in i.section_details if x.split(' /% ')[2] != '' and x.split(' /% ')[1] != '']

        # strip the traling comma
        for section in encoded_sections:
            if section[2].endswith(','):
                section[2] = section[2].rstrip(',')

        temp["sections"] = encoded_sections
        temp["name"] = i.first_name + " " + i.last_name
    
    schedule = Schedule.objects.get(pk=schedule_id)
    schedule_data = get_schedule(schedule)
    context = {
        'instructors_data': data,
        'schedule_courses': schedule_data[0],
        'schedule_credits': schedule_data[1],
        'schedule_ratings': schedule_data[2],
        'schedule_difficulty': schedule_data[3]
        }
    return render(request, "schedule/schedule_with_sections.html", context)


@login_required
def schedule_add_course(request):
    ''' Add a course to a schedule, the request should be FormData for the SectionForm class '''

    if request.method == "POST":
        # Parse the JSON-encoded 'selected_course' field
        try:
            selected_course = json.loads(request.POST.get('selected_course', '{}'))  # Default to empty dict if not found
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        
        form_data = {
            'schedule': request.POST.get('schedule_id'),
            'instructor': int(selected_course.get('instructor')),
            'section': int(selected_course.get('section')),
            'time': selected_course.get('section_time')
        }
        
        # make form object with our passed in data
        form = SectionForm(form_data)

        if form.is_valid():
            scheduled_course = form.save(commit=False)
            # extract id's for all related fields
            schedule_id = form.cleaned_data['schedule'].id  # get the schedule's primary key
            instructor_id = form.cleaned_data['instructor'].id  # get the instructor's primary key
            section_id = form.cleaned_data['section'].id  # get the section's primary key
            course_time = form.cleaned_data['time']

            # update the form object with the related objects returned from the database
            # Note: there might be some optimzation where we could do the request in
            # bulk instead of 4 seperate queries
            scheduled_course.schedule = Schedule.objects.get(id=schedule_id)
            scheduled_course.instructor = Instructor.objects.get(id=instructor_id)
            scheduled_course.section = Section.objects.get(id=section_id)
            scheduled_course.time = course_time
            scheduled_course.save()
        else:
            messages.error(request, "Invalid form data")
            return JsonResponse({'status': 'error'}, status=400)

    messages.success(request, "Succesfully added course!")
    return JsonResponse({'status': 'success'})
