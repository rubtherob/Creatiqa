from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
# Подключаем статус
import random
from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
# Подключаем модель User
from .models import User
from sms import send_sms
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, UserSerializer, UserVerifySerializer




# Создаём класс RegistrUserView
class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    def verify_pin(self, length=5):
        # return random.sample(range(10 ** (length - 1), 10 ** length), 1)[0]
        return 12345

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            user.activate_code = self.verify_pin()
            user.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            send_sms(
                user.activate_code,
                'Creatiqa',
                serializer.data['phone'],
                fail_silently=False
            )
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


@api_view(['GET', 'PUT'])
def verify(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if str(request.data) == user.activate_code:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)