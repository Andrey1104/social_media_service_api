from django.db import models

from social_media_service.settings import AUTH_USER_MODEL
from utils.path_finder import image_file_path


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField(null=True, upload_to=image_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "posts"

    def __str__(self) -> str:
        return f"title: {self.title}, content: {self.content}"


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "comments"

    def __str__(self) -> str:
        return str(self.content)


class Like(models.Model):
    who_liked = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE, null=True
    )
    comment = models.ForeignKey(
        Comment, related_name="likes", on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name_plural = "likes"
        unique_together = ("who_liked", "post") or ("who_liked", "comment")

    def __str__(self) -> str:
        return str(self.who_liked)


class Follower(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "followers"
        unique_together = ("user", "follower")


class Message(models.Model):
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField()
    receiver = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.author}: \n {self.text} \n {self.created_at}"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    participant = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

