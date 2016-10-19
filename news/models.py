#coding:utf-8
from django.db import models
from django.contrib import auth
import datetime
from DjangoUeditor.models import UEditorField
# Create your models here.


class Article(models.Model):
    title = models.CharField('标题', max_length=50)
    subhead = models.CharField('副标题', blank=True, null=True, max_length=50)
    introduction = models.CharField('导语', blank=True, null=True, max_length=200)
    content = UEditorField('正文', height=300, width=1000,default=u'', blank=True, imagePath="uploads/images/",toolbars='besttome', filePath='uploads/files/')
    author = models.CharField('作者', max_length=10, blank=True, null=True,)
    editor = models.CharField('编辑', max_length=10, blank=True, null=True,)
    photographer = models.CharField('摄影', max_length=10, blank=True, null=True,)
    cover = models.CharField('封面图片路径', max_length=100, blank=True, null=True,)
    create_time = models.DateTimeField('创建时间', default=datetime.datetime.now())
    category = models.ManyToManyField('Category')
    is_check = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def _get_view(self):
        return View.objects.filter(article_id=self.id).count()
    views = property(_get_view)

    def _get_like(self):
        return Like.objects.filter(article_id=self.id).count()
    likes = property(_get_like)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ('-id',)


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class View(models.Model):
    article = models.ForeignKey('Article', related_name='view_article')
    view_ip = models.CharField(max_length=20)

    class Meta:
        unique_together = ('article', 'view_ip')


class Like(models.Model):
    article = models.ForeignKey('Article', related_name='like_article')
    like_ip = models.CharField(max_length=20)

    class Meta:
        unique_together = ('article', 'like_ip')
