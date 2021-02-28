# pylint: disable=no-self-use, unused-argument, too-few-public-methods
"""Views for user profile."""

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count, F, Q
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from .browse import safe_round
from ..models import Review, User, SavedCourse


class ProfileForm(ModelForm):
    """Form updating user profile."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'graduation_year']

        # Add the form-control class to make the form work with Bootstrap
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'}),
            'graduation_year': forms.NumberInput(
                attrs={
                    'class': 'form-control'})}


@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            label_suffix='',
            instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
        else:
            messages.error(request, form.errors)
        return HttpResponseRedirect('/profile')

    form = ProfileForm(label_suffix='', instance=request.user)
    return render(request, 'profile/profile.html', {'form': form})


@login_required
def reviews(request):
    """User reviews view."""
    # Handled separately because it requires joining 1 more table (i.e. Vote)
    upvote_stat = Review.objects.filter(user=request.user).aggregate(
        total_review_upvotes=Count('vote', filter=Q(vote__value=1)),
    )
    # Get other statistics
    other_stats = User.objects.filter(id=request.user.id).aggregate(
        total_reviews_written=Count('review'),
        average_review_rating=(
            Avg('review__instructor_rating') +
            Avg('review__enjoyability') +
            Avg('review__recommendability')
        ) / 3,
    )
    # Merge the two dictionaries (NOTE: can be simplified in Python 3.9)
    merged = {**upvote_stat, **other_stats}
    # Round floats
    stats = {key: safe_round(value) for key, value in merged.items()}
    return render(request, 'reviews/user_reviews.html', context=stats)


@login_required
def saved_courses(request):
    """User courses view."""
    # get user courses
    saved_course_instances = SavedCourse.objects.raw('''
        SELECT sc.id
            , sc.course_id
            , sc.instructor_id
            , sc.notes
            , AVG(cig.average) AS average_gpa
            , AVG(r.difficulty) AS average_difficulty
            , (AVG(r.instructor_rating) + AVG(r.enjoyability) + AVG(r.recommendability)) / 3 AS average_rating
            , MAX(CONCAT(INITCAP(s2.season), ' ', s2.year)) AS semester_last_taught
        FROM tcf_website_savedcourse AS sc
        LEFT OUTER JOIN tcf_website_courseinstructorgrade AS cig
            ON sc.course_id = cig.course_id
            AND sc.instructor_id = cig.instructor_id
        LEFT OUTER JOIN tcf_website_review AS r
            ON sc.course_id = r.course_id
            AND sc.instructor_id = r.instructor_id
        INNER JOIN (
            SELECT course_id
                , instructor_id
                , MAX(semester_id) AS semester_id
            FROM tcf_website_section s
            INNER JOIN tcf_website_section_instructors AS si
                ON s.id=si.section_id
            GROUP BY course_id, instructor_id
        ) AS s
            ON sc.course_id = s.course_id
            AND sc.instructor_id = s.instructor_id
        INNER JOIN tcf_website_semester AS s2
            ON s.semester_id=s2.id
        WHERE sc.user_id = %s
        GROUP BY sc.id, sc.course_id, sc.instructor_id, sc.notes
        ORDER BY sc.rank DESC
    ;''', [request.user.id])

    courses = {}
    for saved in saved_course_instances:
        if saved.course.subdepartment in courses:
            courses[saved.course.subdepartment].append(saved)
        else:
            courses[saved.course.subdepartment] = [saved]
    return render(request, 'course/user_courses.html', {'courses': courses})


class SavedCourseReorderingView(View):
    """View for reordering SavedCourse instances"""
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Ensures that the rank is just lower than that of the SavedCourse
        instance with the given `successor_id`. If `successor_id` is not
        supplied, the ranks of all SavedCourse instances will be incremented.
        """
        # Lock the user's saved courses
        saved = SavedCourse.objects.select_for_update().filter(user=request.user)

        try:
            to_move_id = int(request.POST.get('to_move_id'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest('`to_move_id` must be an `int`.')
        to_move = get_object_or_404(
            SavedCourse, pk=to_move_id, user=request.user)
        try:
            successor_id = int(request.POST.get('successor_id'))
        except ValueError:  # str
            return HttpResponseBadRequest('`successor_id` must be an `int`.')
        except TypeError:  # None
            # Everything whose ID >= `successor_id` will be pushed back by 1
            successor_id = 0
            to_move.rank = 1
        else:  # validate successor_id is provided
            successor = get_object_or_404(
                SavedCourse, pk=successor_id, user=request.user)
            to_move.rank = successor.rank

        try:
            with transaction.atomic():
                saved.filter(id__gte=successor_id).update(rank=F('rank') + 1)
                to_move.save()
        except IntegrityError:
            return HttpResponse('Reordering failed...', status_code=500)
        return HttpResponse('Reordering successful!')
