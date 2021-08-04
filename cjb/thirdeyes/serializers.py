from rest_framework import serializers
from .models import Thirdeyes

class ThirdeyesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thirdeyes
        fields = '__all__'
        