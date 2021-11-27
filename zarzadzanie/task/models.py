from django.db import models
from .database import Database as Db



class Projects(models.Model):
    project = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.project}"

class Task(models.Model):

    WEIGHT = {(0, 'minor'), (1, 'major'), (2, 'critical')}
    LEVEL = {(0, 'easy'), (1, 'medium'), (2, 'hard')}
    STATUS = {(0, 'not started'), (1, 'in progress'), (2, 'done')}
    BRANCH = {(0, 'todo'), (1, 'potencjalne bledy uzytkownika'),
              (2, 'znalezione bledy')}

    title = models.CharField(max_length=255, unique=True)
    task = models.TextField()
    branch = models.IntegerField(choices=BRANCH)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    timeneed = models.IntegerField()
    timedone = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    weight = models.IntegerField(choices=WEIGHT)
    level = models.IntegerField(choices=LEVEL)
    status = models.IntegerField(choices=STATUS)
    projekt = models.ForeignKey(Projects, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.id} - {self.title} : {self.created}"

