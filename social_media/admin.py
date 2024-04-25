from django.contrib import admin

from social_media.models import Post, Comment, Like, Follower, Event, Message

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Event)
admin.site.register(Message)
