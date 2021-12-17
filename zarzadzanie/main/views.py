from django.shortcuts import HttpResponse, render, get_list_or_404, redirect
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
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timeusing']

def start(request):

    projects = Projects.objects.all()

    return render(request, "main/strona_startowa.html", {"projects": projects})

def zadania(request, projekt_id: int):
    global no_project

    no_project = projekt_id
    print(f"numer projektu : {no_project}")
    zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "show"}

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


    return render(request, 'main/add_task.html', {'form': form,
                                                  'numer_projektu':  no_project,
                                                  'side': 'add'})

def edytuj_task(request):
    task = get_list_or_404(Task, pk=id)
    form = TaskForm(request.POST or None, instance=Task)
    if form.is_valid():
        form.save()
        return redirect(start)

    return render(request, 'main/add_task.html', {'form': form, "side": "edit"})

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

def delete_task(request, projekt_id: int):
    global no_project

    no_project = projekt_id
    print(f"numer projektu : {no_project}")
    zadania = Task.objects.all().filter(projekt=projekt_id)
    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "delete"}

    return render(request, "main/lista_zadan.html", contex)

def done_task(request, projekt_id: int):
    global no_project

    no_project = projekt_id
    print(f"numer projektu : {no_project}")
    zadania = Task.objects.all().filter(projekt=projekt_id, status=2)
    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "done"}

    return render(request, "main/lista_zadan.html", contex)

def remove_task(request, zadanie_id: int):
    print(f"zadanie o numerze {zadanie_id} usunięto")
    projects = Projects.objects.all()

    task_to_delete = Task.objects.filter(id=zadanie_id)
    task_to_delete.delete()


    return render(request, "main/strona_startowa.html", {"projects": projects})

