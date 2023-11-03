from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from .models import User

import json

DEFAULT_TITLE = 'DjangoDev'


def home(request: HttpRequest):
    data = create_base_data()
    return render(request, 'index.html', data)


def register(request: HttpRequest):
    data = create_base_data('Регистрация')

    if request.method == 'POST':
        post = request.POST

        user = User()
        user.username = post.get('username', '')
        user.email = post.get('email', '')
        password = post.get('password', '')

        data['username'] = user.username
        data['email'] = user.email

        def check_validate():
            if len(user.username) < 3:
                data['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                data['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                data['error'] = '* Пароль должен состоять как минимум из 3 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', data)

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('home')

    return render(request, 'registration/register.html', data)


def user_login(request: HttpRequest):
    data = create_base_data('Вход')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            data['error'] = '* Неверное имя пользователя или пароль'
            return render(request, 'registration/login.html', data)

    return render(request, 'registration/login.html')


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


# Help functions
def create_base_data(title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'title': title,
    }
