from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_media.models import Follower
from social_media.serializers import FollowerListSerializer

from social_media_service.settings import PASSWORD_LENGTH


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "email", "is_staff", "followers", "avatar", "status")
        read_only_fields = ("is_staff", "followers")
        extra_kwargs = {"password": {"write_only": True, "min_length": PASSWORD_LENGTH}}

    @staticmethod
    def get_followers(user):
        followers = Follower.objects.filter(user=user)
        return FollowerListSerializer(followers, many=True).data

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
