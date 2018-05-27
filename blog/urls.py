from django.urls import path, re_path
from . import views

app_name = "blog"
urlpatterns = [
    # https:localhost:8000/blog/1
    path("", views.blog_list, name="blog_list"),
    path("<int:blog_id>", views.blog_detail, name="blog_detail"),
    path("type/<int:id>", views.blogs_with_type, name="blog_with_type"),
    path("date", views.blogs_with_date, name="blog_with_date"),
    path("about", views.about_me, name="about_me")
]