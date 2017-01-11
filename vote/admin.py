from django.contrib import admin
from .models import PhotographicWorkItem, PhotoItem, VoteItem, Group


class VoteItemAdmin(admin.ModelAdmin):
    list_display = ('school_id', 'photographic_work_item', 'create_time')
    search_fields = ['school_id', ]


class PhotographicWorkItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'get_vote_num')
    list_filter = ('group',)

    def get_vote_num(self, obj):
        return VoteItem.objects.filter(photographic_work_item=obj).count()

    get_vote_num.admin_order_field = 'PhotographicWorkItem__get_vote_num'
    get_vote_num.short_description = 'Vote num'


admin.site.register(PhotoItem)
admin.site.register(PhotographicWorkItem, PhotographicWorkItemAdmin)
admin.site.register(VoteItem, VoteItemAdmin)
admin.site.register(Group)
