from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from task.models import Task, Projects

def start(request):

    projects = Projects.objects.all()

    return render(request, "main/strona_startowa.html", {"projects": projects})

def zadania(request, projekt_id: int):

    zadania = Task.objects.all().filter(projekt=projekt_id)
    contex = {"zadania": zadania}
    return render(request, "main/lista_zadan.html", contex)

def details(request):

    return render(request, "main/details.html")

def add_task(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = {
            'title': request.POST['title'],
            'task': request.POST['task'],
            'branch': 0,
            'timeneed': 60,
            'weight': 0,
            'level': 0,
            'status': 0,
            'projekt_id': 4,
        }
        task = Task.objects.create(**data)

    return render(request, 'main/add_task.html', {})

def check_task(request, zadanie_id: int):
    print(zadanie_id)
    return render(request, "main/check_task")