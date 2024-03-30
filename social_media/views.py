from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from social_media.models import Post, Comment, Like, Follower, Message, Event
from social_media.serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowerSerializer,
    MessageSerializer,
    EventSerializer
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     queryset = Post.objects.filter(author=self.request.user)
    #     return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowGroupViewSet(ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
