import string

from django.contrib.auth.models import Group
from rest_framework import serializers
# Подключаем модель user
from pattern.models import Pattern


class PatternSerializer(serializers.ModelSerializer):
    # Настройка полей
    img = serializers.ImageField()
    class Meta:
        # Поля модели которые будем использовать
        model = Pattern
        # Назначаем поля которые будем использовать
        fields = ['group', 'img']

