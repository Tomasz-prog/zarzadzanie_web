from django.shortcuts import render, get_list_or_404, redirect
from task.models import Task, Projects
from django.forms import ModelForm
from django.contrib import messages
# from .models import Task

global no_project

class ProjektForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['project']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status']

def start(request):

    projects = Projects.objects.all()

    return render(request, "main/strona_startowa.html", {"projects": projects})

def zadania(request, projekt_id: int):
    global no_project

    no_project = projekt_id
    print(f"numer projektu : {no_project}")
    zadania = Task.objects.all().filter(projekt=projekt_id)
    contex = {"zadania": zadania, "nr_projektu": projekt_id}

    return render(request, "main/lista_zadan.html", contex)

def details(request):

    return render(request, "main/details.html")

def add_task(request):
    global no_project
    form = TaskForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.projekt_id = no_project
        obj.save()


    return render(request, 'main/add_task.html', {'form': form, 'numer_projektu':  no_project})

def edytuj_task(request):
    task = get_list_or_404(Task, pk=id)
    form = TaskForm(request.POST or None, instance=Task)
    if form.is_valid():
        form.save()
        return redirect(start)

    return render(request, 'main/add_task.html', {'form': form})

def check_task(request, zadanie_id: int):
    # zadania = Task.objects.all().filter(id=zadanie_id)
    # contex = {"zadania": zadania}
    # return render(request, "main/check_task.html", contex)

    global no_project
    task = Task.objects.get(id=zadanie_id)
    no_project = task.projekt_id
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        # return redirect("lista_zadan.html")

    return render(request, 'main/add_task.html', {'form': form, 'numer_projektu':  no_project})

def add_projekt(request):

    form = ProjektForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

    return render(request, 'main/add_projekt.html', {'form': form})

