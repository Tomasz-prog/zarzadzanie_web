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


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timeusing']