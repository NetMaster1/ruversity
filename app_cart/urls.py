from django.urls import path
from . import views

urlpatterns = [
    # path('<int:subject_id>', views.payment_page, name='payment_page'),
    path('pay_pal/<int:subject_id>', views.pay_pal, name='pay_pal'),
    path('credit_card/<int:subject_id>', views.credit_card, name='credit_card'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('qiwi_payment_complete/', views.qiwi_payment_complete, name='qiwi_payment_complete'),
    path('cancel', views.payment_cancel, name='payment_cancel'),
    path('error', views.payment_error, name='payment_error'),
    path('GeneratePDF_invoice/<subject_id>', views.GeneratePDF_invoice.as_view(), name="GeneratePDF_invoice"),

]
