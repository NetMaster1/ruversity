from django.contrib import admin
from . models import MainSubject, Transaction, Price, Category, Language, Rating, Keyword, Lecture, Section, Badword, Credit_card, Credit_card_type, Paypal, Main_method, Cart, Bank_account, DiscountOn, Question, Answer, AdditionalMaterialLink, AdditionalMaterialFile


class MainSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'percent', 'date_posted', 'author', 'author_price', 'ready')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')

class LectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'title', 'video_file', 'author', 'date_posted', 'size_mb', 'length')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'course', 'author', 'money_paid', 'payment_id', 'date_paid', 'paid_amount', 'buyer', 'money_transfer', 'date_transfer', 'transferred_amount')
    list__filter = ('money_paid', 'money_transfer')
    ordering = ('-date_paid',)
    list_per_page=100

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

class DiscountOnAdmin(admin.ModelAdmin):
    list_display = ('id', 'discount_on')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')

class AdditionalMaterialLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'lecture', 'url_link',)

class AdditionalMaterialFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'lecture', 'additional_file',)

admin.site.register(MainSubject, MainSubjectAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Badword, BadwordAdmin)
admin.site.register(Credit_card, Credit_cardAdmin)
admin.site.register(Credit_card_type, Credit_card_typeAdmin)
admin.site.register(Paypal, PaypalAdmin)
admin.site.register(Main_method, Main_methodAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Bank_account, Bank_accountAdmin)
admin.site.register(DiscountOn, DiscountOnAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AdditionalMaterialLink, AdditionalMaterialLinkAdmin)
admin.site.register(AdditionalMaterialFile, AdditionalMaterialFileAdmin)

