from rest_framework import serializers

from social_media.models import Post, Comment, Like, Follower, Message, Event


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "who_liked", "post", "comment")


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("id", "user", "follower")


class FollowerListSerializer(FollowerSerializer):
    follower = serializers.SlugField(source="user.email", read_only=True)

    class Meta:
        model = Follower
        fields = ("id", "follower")


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "likes",
            "author",
            "image",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes(post):
        likes = Like.objects.filter(post=post)
        return LikeSerializer(likes, many=True).data


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "content", "image")


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "post",
            "author",
            "likes",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes(comment):
        likes = Like.objects.filter(comment=comment)
        return LikeSerializer(likes, many=True).data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "description", "participant", "start_date", "end_date")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "author", "text", "receiver", "created_at", "updated_at")
