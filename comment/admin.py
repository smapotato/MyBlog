from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id","content_object",  "content", "comment_time", "user")
