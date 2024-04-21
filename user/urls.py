from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView, TokenBlacklistView,
)

from user.views import CreateUserView, ManageUserView, UserListView, UserImageView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("me/upload_image", UserImageView.as_view(), name="upload_image"),
    path("all/", UserListView.as_view({"get": "list"}), name="user_list"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
