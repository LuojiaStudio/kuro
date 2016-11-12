from django.contrib import admin
from .models import PhotographicWorkItem, PhotoItem, VoteItem, Group


class VoteItemAdmin(admin.ModelAdmin):
    list_display = ('school_id', 'photographic_work_item', 'create_time')
    search_fields = ['school_id', ]


admin.site.register(PhotoItem)
admin.site.register(PhotographicWorkItem)
admin.site.register(VoteItem, VoteItemAdmin)
admin.site.register(Group)
