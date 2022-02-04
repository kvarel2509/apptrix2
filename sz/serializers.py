from rest_framework import serializers
from .models import User


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)


class ReturnClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender')