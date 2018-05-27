import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogType, Blog
from comment.models import Comment

register = template.Library()


# 获取博客分类对应博客数量
@register.filter("count")
def Count(value):
    return Blog.objects.filter(blog_type=value).count()


# 获取时间分类对应的博客
@register.filter("time_count")
def Time_count(value):
    return Blog.objects.filter(create_time__year=value.year, create_time__month=value.month)


# 获取评论数
@register.filter("comment_sum")
def Comment_sum(value):
    blog = ContentType.objects.get_for_model(value)
    return Comment.objects.filter(content_type=blog, object_id=value.pk).count()

