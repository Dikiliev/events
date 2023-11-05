from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from .models import User, Event, EventCategory

import json

DEFAULT_TITLE = 'DjangoDev'


def home(request: HttpRequest):
    data = create_base_data()
    return render(request, 'index.html', data)


def events(request: HttpRequest):
    data = create_base_data('Мероприятия')

    data['categories'] = EventCategory.objects.all()

    _events = Event.objects.all()
    categories = [event.get_category_title() for event in _events]
    periods = [event.get_date_period() for event in _events]

    data['events'] = [{'this': _events[i], 'category': categories[i], 'period': periods[i]} for i in range(len(_events))]

    return render(request, 'events.html', data)


def event(request: HttpRequest, _id: int):
    data = create_base_data('Мероприятие')

    try:
        event = Event.objects.get(id=_id)

        data['event'] = event
        data['category'] = event.get_category_title()
        data['period'] = event.get_date_period()

    except Exception as e:
        return 'Not Found 404'

    return render(request, 'event.html', data)


def create_event(request: HttpRequest):
    data = create_base_data('Новое мероприятие')

    if request.method == 'POST':
        post = request.POST

        event = Event()
        event.creater_id = request.user.id
        event.category_id = EventCategory.objects.get(title=post.get('category')).id

        event.title = post.get('title', '')
        event.description = post.get('description', '')
        event.address = post.get('address', '')
        event.start_date = post.get('start_date', '')
        event.end_date = post.get('end_date', '')
        event.price = post.get('price', 0)

        if not event.price:
            event.price = 0

        uploaded_image = request.FILES.get('image_file', None)
        event.image.save(uploaded_image.name, uploaded_image)

        event.save()

        return redirect('events')

    data['categories'] = EventCategory.objects.all()

    return render(request, 'create_event.html', data)


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
