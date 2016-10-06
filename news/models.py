from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50)
    subhead = models.CharField(blank=True, null=True, max_length=50)
    introduction = models.CharField(blank=True, null=True, max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=10)
    editor = models.CharField(max_length=10)
    photographer = models.CharField(max_length=10)
    views = models.IntegerField()
    likes = models.IntegerField()
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
