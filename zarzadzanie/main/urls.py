from django.urls import path
from .views import start, zadania, details, add_task, check_task, edytuj_task, add_projekt

app_name = 'main'
urlpatterns = [
    path('<int:projekt_id>', zadania, name="zadania"),
    path('main/<int:zadanie_id>', check_task, name="check_task"),

    path('main/details', details, name="details"),
    path('main/add_task', add_task, name="add_task"),
    path('main/add_projekt', add_projekt, name="add_projekt"),
    path('main/edytuj_task/<int:id>/', edytuj_task, name="edytuj_task"),
    path('', start, name="start"),

]


