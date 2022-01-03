from django.urls import path, include
from .views import start, zadania, details, \
    add_task, check_task, edytuj_task, add_projekt, \
    delete_task, remove_task, done_task, add_users, \
    rejestracja, logowanie, wylogowanie, login_view
from django.contrib.auth import views as auth_views



app_name = 'main'
urlpatterns = [
    path('<int:projekt_id>', zadania, name="zadania"),
    path('main/<int:zadanie_id>', check_task, name="check_task"),

    path('main/details', details, name="details"),
    path('main/add_task', add_task, name="add_task"),
    path('main/add_projekt', add_projekt, name="add_projekt"),
    path('main/add_users', add_users, name="add_users"),
    path('main/edytuj_task/<int:id>/', edytuj_task, name="edytuj_task"),
    path('main/remove_task/<int:zadanie_id>/', remove_task, name="remove_task"),
    path('main/delete_task/<int:projekt_id>/', delete_task , name="delete_task"),
    path('main/done_task/<int:projekt_id>/', done_task , name="done_task"),
    path('main/rejestracja', rejestracja, name="rejestracja"),
    path('main/login', login_view, name="login"),
    path('main/wylogowanie', wylogowanie , name="wylogowanie"),
    # path('main/login', auth_views.LoginView.as_view(), name="login"),
    path('main/logout', auth_views.LogoutView.as_view(), name="logout"),
    path('', start, name="start"),


]
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]


