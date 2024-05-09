from rest_framework import serializers
from .models import *


"""User model serializer"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        # Set is_active to False during signup
        validated_data['is_active'] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user


