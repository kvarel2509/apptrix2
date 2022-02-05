from rest_framework import serializers
from .models import User
from .utils import edit_image


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'avatar', 'gender')

    def create(self, validated_data):
        validated_data['avatar'] = edit_image(validated_data['avatar'])
        return User.objects.create_user(**validated_data)


class ReturnClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender')