

# Create your models here.
from django.db import models  # Подключаем работу с моделями
from phone_field import PhoneField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, User

# Создаем класс менеджера пользователей
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    # Создаём метод для создания пользователя
    def _create_user(self, email, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Делаем пользователя
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, password):
        # Возвращаем нового созданного пользователя
        return self._create_user(email, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, password):
        # Возвращаем нового созданного админа
        return self._create_user(email, password, is_staff=True, is_superuser=True)


# Создаём класс User
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)  # Идентификатор
    email = models.EmailField(max_length=100, unique=True)  # Email
    first_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа
    phone = PhoneField(help_text='Contact phone number')
    activate_code = models.CharField(max_length=5, blank=True)


    USERNAME_FIELD = 'email'  # Идентификатор для обращения

    objects = MyUserManager()  # Добавляем методы класса MyUserManager

    # Метод для отображения в админ панели
    def __str__(self):
        return self.email
