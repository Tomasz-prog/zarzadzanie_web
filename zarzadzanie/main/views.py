from django.shortcuts import HttpResponse, render, get_list_or_404, redirect
from task.models import Task, Projects
from django.forms import ModelForm
from django import forms
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, get_user_model, login, logout)

# from .models import Task

global no_project



User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='confirm address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email(self):

        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email is already being used"
            )
        return email



def login_view(request):

    global numer_usera
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        print('logowanie')
        uzytkownik = User.objects.get(username=username)
        numer_usera = uzytkownik.id
        projects = Projects.objects.filter(user=uzytkownik.id)
        contex = {"projects": projects, "user_id": uzytkownik.id}
        if next:
            return redirect(next)
        return render(request,'strona_startowa.html', contex)

    contex = {
        'form': form,
    }
    return render(request, "login.html", contex)


class MySignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(MySignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()

        return user

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

def wylogowanie(request):
    obj = 'something'
    print('wylogowanie')
    return redirect('https://google.com')

def logowanie(request):
    pass
    # if request.method == "POST":
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #
    #     user = authenticate(request, username=username, password=password)
    #
    #     if user is not None:
    #         login(request, user)
    #         contex = {'logowanie': 'ok'}
    #         print('wszystko dziala')
    #         print(f"drukowanie usera w konsoli zalogowanego {user.username}")
    #         # return redirect('strona_startowa.html')
    #         messages.success(request, f"Uzytkownik {user} został zalogowany")
    #         return render(request, 'main/strona_startowa.html', contex)
    # contex = {}
    #
    # return render(request, 'main/login.html', contex)

def rejestracja(request):

    if request.method == 'POST':
        form = MySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Konto zostało założone dla " + user)

    form = MySignUpForm()
    contex = {'form': form}
    return render(request, 'main/register.html', contex)





class ProjektForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['project']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timedone']

def add_users(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

    return render(request, 'main/add_users.html', {'form': form})

@login_required
def start(request):
    try:
        global numer_usera

        projects = Projects.objects.filter(user=numer_usera)
    except:
        projects = None

    return render(request, "strona_startowa.html", {"projects": projects})

@login_required
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
@login_required
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
@login_required
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

@login_required
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
@login_required
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

@login_required
def remove_task(request, zadanie_id: int):
    print(f"zadanie o numerze {zadanie_id} usunięto")
    projects = Projects.objects.all()

    task_to_delete = Task.objects.filter(id=zadanie_id)
    task_to_delete.delete()


    return render(request, "main/strona_startowa.html", {"projects": projects})

