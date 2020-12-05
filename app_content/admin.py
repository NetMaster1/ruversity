from django.contrib import admin
from . models import MainSubject, Transaction, Price, Category, Language, Bestseller, AverageRating


class MainSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted', 'author')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'buyer', 'paid_amount')

# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'subject', 'user', 'rating')

class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'regular', 'discount')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class BestsellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'transactions')

class AverageRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'average')

admin.site.register(MainSubject, MainSubjectAdmin)
admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(Rating, RatingAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Bestseller, BestsellerAdmin)
admin.site.register(AverageRating, AverageRatingAdmin)
