from django.db import models
from django.contrib import auth
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    subhead = models.CharField(blank=True, null=True, max_length=50)
    introduction = models.CharField(blank=True, null=True, max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=10, blank=True, null=True,)
    editor = models.CharField(max_length=10, blank=True, null=True,)
    photographer = models.CharField(max_length=10, blank=True, null=True,)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    category = models.ManyToManyField('Category', blank=True, null=True)
    is_check = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
