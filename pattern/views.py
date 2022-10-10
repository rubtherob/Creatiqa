from django.shortcuts import render

# Create your views here.
from requests import Response


from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from pattern.models import Pattern
from pattern.serializers import PatternSerializer


class PatternViewSet(ModelViewSet):
    # Добавляем в queryset

    queryset = Pattern.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = PatternSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]


