from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, TextField, CharField, BooleanField, IntegerField, JSONField, ImageField, DateTimeField

import locale


locale.setlocale(locale.LC_TIME, 'ru_RU')


class User(AbstractUser):

    class Role:
        visitor = 0
        organizer = 1
        admin = 100

    role = IntegerField(default=Role.visitor)
    avatar = ImageField(blank=True)

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def exist(self):
        return len(User.objects.filter(username=self.username)) > 0


class Event(Model):
    creater_id = IntegerField()
    category_id = IntegerField()

    title = CharField(max_length=255)
    description = TextField()
    address = TextField()
    image = ImageField(upload_to='images/')
    start_date = DateTimeField()
    end_date = DateTimeField()
    price = IntegerField()

    date_created = DateTimeField(auto_now_add=True)

    def get_category_title(self):
        return EventCategory.objects.get(id=self.category_id).title

    def get_date_period(self):
        return f'{self.start_date.strftime("%d %b")} - {self.end_date.strftime("%d %b")}'


class EventCategory(Model):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title
