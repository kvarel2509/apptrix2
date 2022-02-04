from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, gender, password=None):
        if not email or not first_name or not gender:
            raise ValueError('Email, first name and gender is required fields')
        user = self.model(email=self.normalize_email(email), first_name=first_name, gender=gender)
        user.set_password(password)
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, first_name, gender, password=None):
        user = self.create_user(email, first_name, gender, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30, blank=True, default='')
    avatar = models.ImageField('Фотография', upload_to='avatar/', blank=True)
    gender = models.CharField('Пол', max_length=30, choices=[('M', 'Man'), ('W', 'Woman')], help_text='M/W')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'gender']
    objects = CustomUserManager()

    def __str__(self):
        return self.email