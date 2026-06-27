from rest_framework import serializers
from .models import LostTable

class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostTable
        fields = '__all__'