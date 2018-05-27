import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from read_statistics.models import ReadNum, ReadDetail


def ReadStatistics(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 文章阅读数
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 当天阅读数
        date = timezone.now().date()
        readDetail, create = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        total = read_details.aggregate(read_num_sum=Sum("read_num"))
        read_nums.append(total["read_num_sum"] or 0)
    return read_nums, dates


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("-read_num")
    return read_detail[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by("-read_num")
    return read_detail[:7]

def popular_articles(content_type):
    # 获取阅读数最多的7篇文章
    sum_articles = ReadNum.objects.filter(content_type=content_type).order_by("-read_num")
    return sum_articles[:7]