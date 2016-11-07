from django.db import models

# Create your models here.


class PhotographicWorkItem(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey('Group')

    def _get_vote(self):
        return VoteItem.objects.filter(photographic_work_item_id=self.id).count()
    vote = property(_get_vote)

    def __str__(self):
        return self.name


class PhotoItem(models.Model):
    photographic_work_item = models.ForeignKey('PhotographicWorkItem')
    path = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class VoteItem(models.Model):
    school_id = models.CharField(max_length=15)
    photographic_work_item = models.ForeignKey('PhotographicWorkItem')
    create_time = models.DateTimeField(auto_now_add=True)


