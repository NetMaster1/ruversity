from django.contrib import admin
from . models import MainSubject


class MainSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted', 'author')


admin.site.register(MainSubject, MainSubjectAdmin)
