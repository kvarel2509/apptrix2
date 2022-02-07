from rest_framework import serializers
from .models import User
from .utils import edit_image


class ClientSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_value=90, min_value=-90, max_digits=8, decimal_places=6)
    longitude = serializers.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'avatar', 'gender', 'latitude', 'longitude')

    def create(self, validated_data):
        if 'avatar' in validated_data:
            validated_data['avatar'] = edit_image(validated_data['avatar'])
        return User.objects.create_user(**validated_data)


class ReturnClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'latitude', 'longitude')


class ReturnClientsListSerializer(serializers.ModelSerializer):
    distance = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'latitude', 'longitude', 'distance')