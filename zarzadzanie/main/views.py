from django.shortcuts import HttpResponse, render, get_list_or_404, redirect
from task.models import Task, Projects
from django.forms import ModelForm
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.models import User


from django.contrib import messages
# from .models import Task

global no_project

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProjektForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['project']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timeusing', 'timedone']

def add_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

    return render(request, 'main/add_users.html', {'form': form})

def start(request):

    all_task = Task.objects.all()
    projects = Projects.objects.all()
    # lista = Projects.objects.values_list()
    # suma_minut_timeneed = []
    # for i in lista:
    #
    #     val = i[0]
    #     suma = Task.objects.filter(projekt_id=val).aggregate(Sum('timeneed'))
    #     suma_minut_timeneed.append(suma)
    # print(suma_minut_timeneed)
    return render(request, "main/strona_startowa.html", {"projects": projects})

def zadania(request, projekt_id: int):
    global no_project

    no_project = projekt_id
    print(f"numer projektu : {no_project}")
    zadania = Task.objects.all().filter(projekt=projekt_id, status__lt=2)
    projekt = Projects.objects.filter(id=no_project)
    name_of_projekt = projekt[0].project
    suma_need = Task.objects.filter(projekt_id=no_project).exclude(status=2).aggregate(Sum('timeneed'))

    if suma_need['timeneed__sum'] != None:

        suma_done_min = Task.objects.filter(projekt_id=no_project).exclude(status=2).aggregate(Sum('timedone'))
        suma_done_done = Task.objects.filter(projekt_id=no_project, status=2).aggregate(Sum('timedone'))

        if suma_done_done["timedone__sum"] == None:
            suma_done_done["timedone__sum"] = 0

        suma_done = round(float((suma_done_min["timedone__sum"]/60)) + float((suma_done_done["timedone__sum"] / 60)), 2)
        suma_czas_do_skonczenia = round((suma_need["timeneed__sum"] - suma_done_min["timedone__sum"])/60, 2)
        info_o_zadaniach = ""
    else:
        suma_czas_do_skonczenia = 0
        suma_done = 0
        info_o_zadaniach = "DODAJ ZADANIE"

    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "show",
              "time_need": suma_czas_do_skonczenia, "time_done": suma_done, "is_task": info_o_zadaniach,
              "nazwa_projektu": name_of_projekt}

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



        zadania = Task.objects.all().filter(projekt=no_project, status__lt=2)
        contex = {"zadania": zadania, "nr_projektu": no_project, "side": "show"}
        return render(request, "main/lista_zadan.html", contex)

    return render(request, 'main/add_task.html', {'form': form,
                                                  'numer_projektu':  no_project,
                                                  'side': 'add'})

def edytuj_task(request):
    task = get_list_or_404(Task, pk=id)
    form = TaskForm(request.POST or None, instance=Task)
    print('edytuje zadanie ')

    if form.is_valid():
        # form.save()

        obj = form.save(commit=False)
        obj.projekt_id = no_project
        obj.timedone = obj.timedone + obj.timeusing
        print('testowanei ponizej')
        print(obj.timedone)
        obj.save()

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
        obj = form.save(commit=False)
        obj.projekt_id = no_project
        obj.timedone = obj.timedone + obj.timeusing

        obj.timeusing = 0
        obj.save()

        # form.save()
        # print('tutaj')
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

    suma_need_done = Task.objects.filter(projekt_id=no_project, status=2).aggregate(Sum('timeneed'))
    suma_timeneed_done = round(suma_need_done["timeneed__sum"] / 60, 2)
    suma_done_done = Task.objects.filter(projekt_id=no_project, status=2).aggregate(Sum('timedone'))
    suma_done_done = round(suma_done_done["timedone__sum"] / 60, 2)

    contex = {"zadania": zadania, "nr_projektu": projekt_id, "side": "done", "suma_timeneed_done": suma_timeneed_done,
              "suma_done_done": suma_done_done}

    return render(request, "main/lista_zadan.html", contex)

def remove_task(request, zadanie_id: int):
    print(f"zadanie o numerze {zadanie_id} usunięto")
    projects = Projects.objects.all()

    task_to_delete = Task.objects.filter(id=zadanie_id)
    task_to_delete.delete()


    return render(request, "main/strona_startowa.html", {"projects": projects})

