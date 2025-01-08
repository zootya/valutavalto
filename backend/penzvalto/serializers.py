from rest_framework import serializers
from .models import Valutak

class ValutakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valutak
        fields="__all__"