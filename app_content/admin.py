from django.contrib import admin
from . models import MainSubject, Transaction, Price, Category, Language, Rating, Keyword, Lecture, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Cart, Bank_account


class MainSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'percent', 'date_posted', 'author')

class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_posted')

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

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'user')

class BadwordAdmin(admin.ModelAdmin):
    list_display = ('id', 'badword')

# class AverageRatingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'subject', 'average', 'av_rating')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'rating', 'user')
    
class Credit_cardAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'card_number', 'card_type' , 'user')

class Credit_card_typeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')

class PaypalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')

class Credit_cardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_number')

class Main_methodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'method')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user')
    
class Bank_accountAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_name', 'account')

admin.site.register(MainSubject, MainSubjectAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Badword, BadwordAdmin)
admin.site.register(Credit_card, Credit_cardAdmin)
admin.site.register(Credit_card_type, Credit_card_typeAdmin)
admin.site.register(Paypal, PaypalAdmin)
admin.site.register(Main_method, Main_methodAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Bank_account, Bank_accountAdmin)

