from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, TextField, CharField, BooleanField, IntegerField, JSONField, ImageField, DateTimeField


class User(AbstractUser):

    class Role:
        student = 0
        teacher = 1
        admin = 100

    role = IntegerField(default=Role.student)
    avatar = ImageField()

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
    start_date = DateTimeField()

    date_created = DateTimeField(auto_now_add=True)


class EventCategory(Model):
    title = CharField(max_length=255)
