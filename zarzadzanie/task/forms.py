# from django import forms
from django.forms import ModelForm
from .models import Task


class Weight():
    MINOR, MAJOR, CRITICAL = 0, 1, 2
    WEIGHT = ((MINOR, 'Minor'), (MAJOR, 'Major'), (CRITICAL, 'Critical'))


class Level():
    EASY, MEDIUM, HARD = 0, 1, 2
    LEVEL = ((EASY, 'Easy'), (MEDIUM, 'Medium'), (HARD, 'Hard'))


class Status():
    NOT_STARTED, IN_PROGRESS, DONE = 0, 1, 2
    STATUS = ((NOT_STARTED, 'Not started'), (IN_PROGRESS, 'In progress'), (DONE, 'Done'))


class Branch():
    TODO, POTTENTIAL_ERRORS, FOUND = 0, 1, 2
    BRANCH = ((TODO, 'todo'), (POTTENTIAL_ERRORS, 'potencjalne błedy użytkownika'), (FOUND, 'znalezione błędy'))


# class TaskForm(ModelForm):
#
#     title = forms.CharField(label="name", max_length=255)
#     task = forms.CharField(label="task")
#     branch = forms.CharField(label='type of task', widget=forms.Select(choices=Branch.BRANCH))
#     timeneed = forms.IntegerField()
#     weight = forms.CharField(label="weight", widget=forms.Select(choices=Weight.WEIGHT))
#     level = forms.CharField(label="level", widget=forms.Select(choices=Level.LEVEL))
#     status = forms.CharField(label="status", widget=forms.Select(choices=Status.STATUS))

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timeusing']