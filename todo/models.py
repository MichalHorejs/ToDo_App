from django.db import models


class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Task(models.Model):
    task = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task
