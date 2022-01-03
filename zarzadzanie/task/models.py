from django.db import models
from .database import Database as Db



class Uzytkownik(models.Model):
    pass


class Projects(models.Model):
    project = models.CharField(max_length=255, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.id} - {self.project}, {self.user}"

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

    TODO, POTTENTIAL_ERRORS, FOUND, IMPLEMENTATIONS, CSS = 0, 1, 2, 3, 4
    BRANCH = ((TODO, 'todo'), (POTTENTIAL_ERRORS, 'potencjalne błedy użytkownika'), (FOUND, 'znalezione błędy'),
              (IMPLEMENTATIONS, 'usprawnienia'), (CSS, 'CSS'))

class Task(models.Model):

    title = models.CharField(max_length=255, unique=True)
    task = models.TextField()
    branch = models.PositiveSmallIntegerField(choices=Branch.BRANCH, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    timeneed = models.IntegerField()
    timedone = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    weight = models.PositiveSmallIntegerField(choices=Weight.WEIGHT, default=0)
    level = models.PositiveSmallIntegerField(choices=Level.LEVEL, default=0)
    status = models.PositiveSmallIntegerField(choices=Status.STATUS, default=0)
    projekt = models.ForeignKey(Projects, on_delete=models.CASCADE, default=None)
    timeusing = models.IntegerField(blank=True, default=0)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.id} - {self.title} : {self.created}"

