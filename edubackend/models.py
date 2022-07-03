from django.db import models

# Create your models here.


class userStudents(models.Model):
    name = models.CharField(max_length=100)