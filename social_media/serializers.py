from rest_framework import serializers

from social_media.models import Post, Comment, Like, Follower, Message, Event


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post", "comment")


class LikeListSerializer(LikeSerializer):
    class Meta:
        model = Like
        fields = ("id", "author")


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("id", "user")


class FollowerListSerializer(FollowerSerializer):
    follower = serializers.SlugField(source="user.email", read_only=True)

    class Meta:
        model = Follower
        fields = ("id", "follower")


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "comments",
            "likes",
            "image",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes(post) -> LikeSerializer:
        likes = Like.objects.filter(post=post)
        return LikeListSerializer(likes, many=True).data

    @staticmethod
    def get_comments(post) -> LikeSerializer:
        comments = Comment.objects.filter(post=post)
        return CommentSerializer(comments, many=True).data


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "image")


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "post",
            "likes",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_likes(comment) -> LikeSerializer:
        likes = Like.objects.filter(comment=comment)
        return LikeListSerializer(likes, many=True).data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "participant",
            "start_date",
            "end_date"
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "text",
            "recipient",
            "created_at",
            "updated_at"
        )


class MessageListSerializer(MessageSerializer):
    class Meta:
        model = Message
        fields = ("id", "author", "text")
