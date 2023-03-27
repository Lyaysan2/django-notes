from django.contrib import admin

from web.models import Note, Tag


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'user', 'created_at', 'updated_at')
    search_fields = ("id", "title", "text")
    list_filter = ('created_at', 'updated_at', "user")
    ordering = ('-updated_at',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "user")
    search_fields = ("id", "name")
    list_filter = ("user",)


admin.site.register(Note, NoteAdmin)
admin.site.register(Tag, TagAdmin)