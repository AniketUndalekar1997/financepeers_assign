from enum import unique
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    # we want to login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):
    p_k = models.AutoField(primary_key=True)
    id = models.IntegerField()
    userId = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
