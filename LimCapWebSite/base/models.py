import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

genders = [
    ("male", "Male"),
    ("female", "Female"),
    ("others", "Others"),
]

countryCodeList = [
    ("+234", "+234"),
    ("+229", "+229"),
]


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=20, default="0")
    description = models.TextField(default="Not Available")

    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    gender = models.CharField(max_length=10, null=False, choices=genders)
    course = models.CharField(null=False, max_length=50)
    # course = models.ForeignKey(Course, on_delete=models.PROTECT)
    countryCode = models.CharField(max_length=5, null=False, choices=countryCodeList)
    phoneNumber = models.CharField(max_length=12)
    email = models.EmailField(max_length=50, null=False, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(default="avatar.svg", blank=True, null=True)
    paymentStatus = models.CharField(max_length=20, default="Not paid", null=False)

    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username}"


class StudyGroup(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} hosted by {self.host}"
