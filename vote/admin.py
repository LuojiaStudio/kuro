from django.contrib import admin
from .models import PhotographicWorkItem, PhotoItem, VoteItem, Group


admin.site.register(PhotoItem)
admin.site.register(PhotographicWorkItem)
admin.site.register(VoteItem)
admin.site.register(Group)
