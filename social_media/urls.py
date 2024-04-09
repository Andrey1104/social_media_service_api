from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    PostViewSet,
    CommentViewSet,
    LikeViewSet,
    FollowGroupViewSet,
    EventViewSet,
    MessageViewSet
)

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("likes", LikeViewSet)
router.register("followers", FollowGroupViewSet)
router.register("events", EventViewSet)
router.register("messages", MessageViewSet)

urlpatterns = [
    path("", include(router.urls))
]
