from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from social_media.models import Post, Comment, Like, Follower, Message, Event
from social_media.permissions import IsOwnerOrAdmin
from social_media.serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowerSerializer,
    MessageSerializer,
    EventSerializer
)


# TODO Users should be able to create new posts with text content
#  and optional media attachments (e.g., images). (Adding images is optional task)
#  Users should be able to retrieve their own posts and posts of users they are following.
#  Users should be able to retrieve posts by hashtags or other criteria.
#  Schedule Post creation using Celery (Optional):
#  Add possibility to schedule Post creation (you can select the time to create the Post before creating of it).


class DestroyMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser and instance.author != request.user:
            raise PermissionDenied("You do not have permission to perform this action...")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateMixin:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(CreateMixin, DestroyMixin, ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        """Retrieve posts with filters"""
        title = self.request.query_params.get("title")
        content = self.request.query_params.get("content")
        author = self.request.query_params.get("author")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if content:
            queryset = queryset.filter(content__icontains=content)

        if author:
            queryset = queryset.filter(author__first_name__icontains=author)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by title (ex. ?title=hello)",
            ),
            OpenApiParameter(
                "content",
                type=OpenApiTypes.STR,
                description="Filter by content (ex. ?content=sunday)",
            ),
            OpenApiParameter(
                "author",
                type=OpenApiTypes.STR,
                description="Filter by author (ex. ?author=Tom)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CommentViewSet(CreateMixin, DestroyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class LikeViewSet(GenericViewSet, CreateModelMixin, DestroyMixin):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class FollowGroupViewSet(CreateMixin, DestroyMixin, ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Follower.objects.filter(user=self.request.user)


class MessageViewSet(CreateMixin, DestroyMixin, ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class EventViewSet(DestroyMixin, ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
