from django.contrib import admin
from . models import Entity, Person


class EntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type', 'name', 'tax_id_number')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone')


admin.site.register(Entity, EntityAdmin)
admin.site.register(Person, PersonAdmin)
