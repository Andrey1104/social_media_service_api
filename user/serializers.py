from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_media.models import Follower, Message
from social_media.serializers import (
    FollowerListSerializer,
    MessageListSerializer
)

from social_media_service.settings import PASSWORD_LENGTH


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {"write_only": True, "min_length": PASSWORD_LENGTH}
        }

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


class UserDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "followers",
            "messages",
            "status",
            "is_premium",
            "avatar"
        )
        read_only_fields = ("is_staff", "followers", "messages", "is_premium")

    @staticmethod
    def get_followers(user) -> FollowerListSerializer:
        followers = Follower.objects.filter(user=user)
        return FollowerListSerializer(followers, many=True).data

    @staticmethod
    def get_messages(user) -> MessageListSerializer:
        messages = Message.objects.filter(recipient=user)
        return MessageListSerializer(messages, many=True).data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "avatar")


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "avatar")
