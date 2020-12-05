from django.shortcuts import render, redirect, get_object_or_404
from app_content.models import MainSubject, Transaction, Bestseller
from hashlib import md5
from django.http import HttpResponse
import json
from django.http import JsonResponse

# Create your views here.


def pay_pal(request, subject_id):
    subject = MainSubject.objects.get(id=subject_id)

    context = {
        'subject': subject
    }
    return render(request, 'cart/pay_pal_page_ver1.html', context)


def payment_complete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    subject = MainSubject.objects.get(id=body['subject_id'])
    Transaction.objects.create(
        course=subject,
        buyer=request.user
    )

    if Bestseller.objects.filter(subject=subject).exists():
        object=Bestseller.objects.get(subject=subject)
        counter = object.transactions + 1
        object.transactions=counter
        object.save()
    else:
        Bestseller.objects.create(
            subject=subject,
            transactions=1
        )

    # context = {
    #     'body': body
    # }
    return JsonResponse('Payment completed!', safe=False)
    # return render(request, 'cart/payment_complete.html', context)


def payment_cancel(request):
    pass


def payment_error(request):
    pass


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
