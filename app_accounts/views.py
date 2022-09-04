from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from app_accounts.models import Entity, Person


def register_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # checking if the user is a person or entity
        customer_type = False
        try:
            if request.POST['customer_type']:
                # if 'entity' in request.GET:
                customer_type = True
        except KeyError:
            customer_type = False
            
        if password == password2:
            # Check user name
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует.')
                return redirect('register_user')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Такой адрес электронной почты уже существует.')
                    return redirect('register_user')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name)

                    # including the user in Person or Entity table
                    if customer_type:
                        if Group.objects.filter(name='entity').exists():
                            entity = Group.objects.get(name='entity')
                        else:
                            Group.objects.create(name='entity').save()
                            entity = Group.objects.get(name='entity')
                        entity.user_set.add(user)
                        Entity.objects.create(user=user).save()
                    else:
                        if Group.objects.filter(name='person').exists():
                            person = Group.objects.get(name='person')
                        else:
                            Group.objects.create(name='person').save()
                            person = Group.objects.get(name='person')
                        person.user_set.add(user)
                        Person.objects.create(user=user).save()

                    # saving the request.user
                    user.save()
                    auth.login(request, user)

                    if Group.objects.filter(name='entity').exists():
                        # if 'entity' in request.user.groups.all:
                        group = Group.objects.get(name='entity').user_set.all()
                        if request.user in group:
                        # or you can use the following structure:
                        #if user.groups.filter(name=entity).count() != 0
                            entity = Entity.objects.get(user=request.user)
                            context = {
                                'entity': entity,
                                'group': group
                            }
                            messages.success(request, 'Вы зарегистрировались как юридическое лицо.')
                            #return redirect('dashboard')
                            return redirect('main_page')
                    #     else:
                    #         person = Person.objects.get(user=request.user)
                    #         context = {
                    #             'person': person,
                    #         }
                        # return render(request, 'accounts/dashboard.html', context)
                        #return redirect('dashboard')
                        return redirect('main_page')
                    else:
                    # person = Person.objects.get(user=request.user)
                    # context = {
                    #     'person': person,
                    # }
                    # return redirect ('dashboard')
                        return redirect('main_page')

                    # Login after register
                    #auth.login(request, user)
                    #messages.success(request, 'You are now logged in')
                    # return redirect ('index')
        else:
            messages.error(request, "Пароли не совпадают. Попробуйте еще раз.")
            return redirect('register_user')
    else:
        return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, ('Your have successfully been logged in. Welcome to ruversity.com'))
            messages.success(request, ('Вы успешно вошли. Добро пожаловать на ruversity.com'))
            return redirect('main_page')
        else:
            #messages.error(request, ('Incorrect username or password. Check your credentials & try again'))
            messages.error(request, ('Неправильное имя пользователи или пароль. Проверьте ваше данные и попробуйте еще раз'))
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    #messages.success(request, ('You are now logged out'))
    messages.success(request, ('Вы вышли из личного кабинета ruversity.com'))
    return redirect('index')


# def dashboard(request):
#     if request.user.is_authenticated:
#         return render(request, 'accounts/dashboard.html')
#     else:
#         return redirect('login')

def change_email(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST['email']
            user = User.objects.get(id=request.user.id)
            if User.objects.filter(email=email).exists():
                 messages.error(
                     request, 'There is a user with this email')
                 return redirect('dashboard')
            else:
                user.email = email
                user.save()
                return redirect ('dashboard')        
    else:
        return redirect ('login')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            # password = request.POST['password']
            new_password_1 = request.POST['new_password_1']
            new_password_2 = request.POST['new_password_2']
            # if password == user.password:
            if new_password_1 == new_password_2:
                user.set_password(new_password_1)
                user.save()
                return redirect('dashboard')
            else:
                messages.error(
                    request, 'Your passwords provided are not the same. Try againg, please')
                return redirect('dashboard')
            # else:
            #     messages.error(
            #         request, 'You provided wrong current password. Try againg, please')
            #     return redirect('dashboard')
    else:
        return redirect('login')


def change_name(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect('dashboard')
    else:
        return redirect('login')
