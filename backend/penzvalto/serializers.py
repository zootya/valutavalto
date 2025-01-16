from rest_framework import serializers
from .models import Valutak, mnb_deviza, mnb_name

class ValutakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valutak
        fields="__all__"

class MnbSerializer(serializers.ModelSerializer):
    class Meta:
        model = mnb_deviza
        fields="__all__"

class MnbNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = mnb_name
        fields="__all__"