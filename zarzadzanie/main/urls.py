from django.urls import path
from .views import start, zadania, details, add_task, check_task

app_name = 'main'

urlpatterns = [
    path('<int:projekt_id>', zadania, name="zadania"),
    path('<int:zadanie_id>', check_task, name="check_task"),
    path('details', details, name="details"),
    path('add_task', add_task, name="add_task"),
    path('', start, name="start")
]

