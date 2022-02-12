from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, gender, latitude, longitude, password=None, **kwargs):
        if not email or not first_name or not gender or not password:
            raise ValueError('Email, first name, gender and password is required fields')
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          gender=gender,
                          latitude=latitude,
                          longitude=longitude,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, gender, latitude, longitude, password=None):
        user = self.create_user(email, first_name, gender, latitude, longitude, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30, blank=True, default='')
    avatar = models.ImageField('Фотография', upload_to='avatar/', blank=True)
    gender = models.CharField('Пол', max_length=30, choices=[('M', 'Man'), ('W', 'Woman')], help_text='M/W')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    match = models.ManyToManyField('self', symmetrical=False, blank=True)
    latitude = models.DecimalField('Широта', max_digits=8, decimal_places=6)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'gender', 'latitude', 'longitude']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
