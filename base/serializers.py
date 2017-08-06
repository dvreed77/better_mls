from rest_framework import serializers
from .models import *



class MLSCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLSComplete
        fields = '__all__'
