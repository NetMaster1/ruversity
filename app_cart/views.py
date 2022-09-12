from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Cart, DiscountOn
from app_accounts.models import Author

from hashlib import md5
from django.http import HttpResponse
import json
from django.http import JsonResponse
from ipstack import GeoLookup

from app_workshop.utils import render_to_pdf
from django.views.generic import View
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.contrib.auth.models import User, Group

import datetime
# Create your views here.


def pay_pal(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)

        context = {
            'subject': subject
        }
        return render(request, 'cart/pay_pal_page_ver1.html', context)
    else:
        return redirect ('login')

def payment_complete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    subject = MainSubject.objects.get(id=body['subject_id'])
    #==============================================================
    Transaction.objects.create(
        course=subject,
        buyer=request.user
    )
    #==============================================================
    counter = subject.transactions + 1
    subject.transactions = counter
    subject.save()

    if Cart.objects.filter(subject=subject, user=request.user).exists():
        cart_item = Cart.objects.get(subject=subject, user=request.user)
        cart_item.delete()
    
        context = {
            'body': body
        }
        return JsonResponse('Payment completed!', safe=False)
        # return redirect('mycourses')
    else:
        context = {
            'body': body
        }
        return JsonResponse('Payment completed!', safe=False)
        # return redirect ('mycourses')

def credit_card(request, subject_id):
    if request.user.is_authenticated:
        subject = MainSubject.objects.get(id=subject_id)
        author=Author.objects.get(id=subject.author)
        author = subject.author.last_name
        discount_time = DiscountOn.objects.get(id=1)
        if Transaction.objects.filter(buyer=request.user, course=subject).exists():
            transaction=Transaction.objects.get(buyer=request.user, course=subject)
        else:
           transaction= Transaction.objects.create(
                course=subject,
                buyer=request.user,
                author=author,
            )
        context = {
            'subject': subject,
            'discount_time': discount_time,
            'transaction':transaction,
        }
        return render(request, 'cart/credit_card.html', context)
    else:
        return redirect ('login')

@csrf_exempt
def qiwi_payment_complete (request):
    if request.method == 'POST':
        id = request.POST.get('id')#unique payment id
        sum = request.POST.get('sum')
        transaction_id = request.POST.get('orderid')
        clientid = request.POST.get('clientid')
        subject = request.POST.get('service_name')
        key = request.POST.get('key')
        # key = request.POST['key']
        secret_word='KLdr[=fjtC4YJb4jf'
        subject=MainSubject.objects.get(id=subject)
        user=User.objects.get(id=1)
    #==============================================================
        transaction=Transaction.objects.get(id=transaction_id)
        if transaction.date_paid is None:
            transaction.paid_amount=sum
            transaction.date_paid=datetime.datetime.now()
            transaction.save()

        string = id + sum + clientid + transaction_id + secret_word
        if key == hashlib.md5(b'string'):
            string=id + secret_word
            print ('OK', hashlib.md5(b'string'))
    #==============================================================
       
        
        return JsonResponse('Payment completed!', safe=False)
        #return render(request, 'cart/qiwi_payment_complete.html')
    else:
        return redirect ('login')


def payment_cancel(request):
    pass


def payment_error(request):
    pass


class GeneratePDF_invoice(View):
    # def get(self, request, *args, **kwargs):
    def get(self, request, subject_id):
        data = {
            # 'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('cart/invoice_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        # return None

# def payment_page(request, subject_id):
#     if request.method == 'GET':
#         user = request.user
#         if not user.is_authenticated:
#             return redirect('login')
#         subject = get_object_or_404(MainSubject, pk=subject_id)
#         secret_key = "sjdfkjksjdkfjskdjfskjdfksdjfk"
#         pid = '3453453'
#         sid = 'CourseSeller'
#         amount = subject.price
#         success = 'http://localhost:8000/cart/payment_success/?subject_id={}'.format(
#             subject_id)
#         cancel = 'http://localhost:8000/cart/cancel'
#         error = 'http://localhost:8000/cart/error'
#         checksumstr = 'pid={}&sid={}&amount={}&token={}'.format(
#             pid, sid, amount, secret_key)
#         digest = md5(checksumstr.encode('ascii'))
#         checksum = digest.hexdigest()
#         url = 'http:///payment.service.com'
#         transaction = Transaction.objects.filter(
#             buyer=request.user.id, course=subject_id)
#         if transaction.count() != 0:
#             return render(request, 'index.html', {'error': 'You have already bought this course'})
#         else:
#             context = {
#                 'subject': subject,
#                 'url': url,
#                 'pid': pid,
#                 'sid': sid,
#                 'amount': amount,
#                 'success': success,
#                 'cancel': cancel,
#                 'error': error,
#                 'checksum': checksum
#             }
#             return render(request, 'cart/payment_page.html', context)
#     else:
#         return HTTPResponse(status=500)

# def payment_success(request):
#     if request.method == 'GET':
#         user = request.user
#         if not user.is_authenticated:
#             return redirect('login')
#         subject_id = request.GET['subject_id']
#         subject = get_object_or_404(MainSubject, pk=subject_id)
#         secret_key = "sjdfkjksjdkfjskdjfskjdfksdjfk"
#         pid = request.GET['subject_id']
#         ref = request.GET['subject_id']
#         result = request.GET['subject_id']
#         checksum = request.GET['subject_id']
#         checksumstr = 'pid={}&ref={}&result={}&token={}'.format(
#             pid, ref, result, secret_key)
#         digest = md5(checksumstr.encode('ascii'))
#         calculated_hash = digest.hexdigest()
#         if calculated_hash == checksum:
#             Transaction.objects.create(
#                 course=subject, buyer=request.user, paid_amount=subject.price).save()
#             return redirect('mycourses')
#         else:
#             return HttpResponse(status=500)
#     else:
#         return HttpResponse(status=500)
