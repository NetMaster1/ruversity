from django.contrib import admin
from . models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content', 'date_posted', 'author')


admin.site.register(Review, ReviewAdmin)
