import markdown, re
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import ReadStatistics, popular_articles
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm

per_page_blogs = 5


def common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, per_page_blogs)
    page_num = request.GET.get("page", 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    page_range = list(
        range(max(current_page_num - 2, 1), min(current_page_num + 3, paginator.num_pages + 1)))  # 防止出现-1，0这样情况
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {
        "blogs": Blog.objects.all(),
        "page_of_blogs": page_of_blogs,
        "page_range": page_range,
        "blog_count": Blog.objects.all().count(),
        "blog_types": BlogType.objects.all(),
        "blog_dates": Blog.objects.dates("create_time", "month", order="DESC")
    }
    return context


def blog_list(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    blogs_all_list = Blog.objects.all()
    context = common_data(request, blogs_all_list)
    context["popular_articles"] = popular_articles(blog_content_type)
    return render(request, "blog/blog_list.html", context=context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    # 浏览器再次刷新时不会更新阅读数
    read_cookie_key = ReadStatistics(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk,
                                      parent=None)
    # 支持markdown语法
    config = {
        'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint linenums',
        }
    }
    # strip_html = re.sub('<[^<]+?>', '', blog.content)
    blog.body = markdown.markdown(blog.content,
                                  extensions=['codehilite'], extension_configs=config)
    data = {
        "content_type": blog_content_type.model,
        "object_id": blog_id,
        "reply_comment_id": 0,
    }
    context = {
        "blog": blog,
        "previous_blog": Blog.objects.filter(create_time__gt=blog.create_time).last(),
        "next_blog": Blog.objects.filter(create_time__lt=blog.create_time).first(),
        "comments": comments.order_by("-comment_time"),
        "comments_count": Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count(),
        "comment_form": CommentForm(initial=data),
        "login_form": LoginForm()
    }
    response = render(request, "blog/blog_detail.html", context)
    response.set_cookie(read_cookie_key, "true")  # 设置cookie
    return response


def blogs_with_type(request, id):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    blog_type = get_object_or_404(BlogType, pk=id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = common_data(request, blogs_all_list)
    context["blog_type"] = blog_type
    context["popular_articles"] = popular_articles(blog_content_type)
    return render(request, "blog/blogs_with_type.html", context=context)


def blogs_with_date(request):
    blogs_all_list = Blog.objects.all()
    context = common_data(request, blogs_all_list)
    return render(request, "blog/blogs_with_date.html", context=context)


def about_me(request):
    return render(request, "blog/about_me.html")