from django.contrib import admin
from . models import Entity, Person, Author


class EntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type', 'name', 'tax_id_number')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Author, AuthorAdmin)
