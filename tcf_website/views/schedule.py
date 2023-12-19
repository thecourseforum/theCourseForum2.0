"""View pertaining to schedule creation/viewing."""

from django import forms
# from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin  # For class-based views
# from django.contrib.messages.views import SuccessMessageMixin
# from django.core.exceptions import PermissionDenied
from django.contrib import messages
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy

from ..models import Schedule, User


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

    # def __init__(self, *args, **kwargs):
    #     super(ScheduleForm, self).__init__(*args, **kwargs)
    #     self.fields['user_id'].required = False


@login_required
def view_schedules(request):
    '''
    get all schedules for a given user
    '''

    return render(request, 'schedule/user_schedules.html')


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
                return render(request, 'schedule/new_schedule.html', {"form": form})
            schedule.save()
            messages.success(request, "Succesfully created schedule!")
            return redirect('schedule')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/new_schedule.html', {"form": form})
