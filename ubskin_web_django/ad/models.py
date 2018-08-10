import time

from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count


class Campaigns(models.Model):
    '''
    活动表
    '''
    campaign_id = models.AutoField(db_column="campaign_id", primary_key=True, verbose_name="活动ID")
    location = models.CharField(db_column="location", verbose_name="活动位置", max_length=255)
    campaign_name = models.CharField(db_column="campaign_name", verbose_name="活动名字", max_length=255)
    start_time = models.IntegerField(db_column="start_time", verbose_name="活动开始时间")
    end_time = models.IntegerField(db_column="end_time", verbose_name="活动结束时间")
    intorduction = models.CharField(db_column="intorduction", verbose_name="活动介绍", max_length=1000, null=True, blank=True)
    campaigns_photo_id = models.CharField(db_column="campaigns_photo_id", verbose_name="活动图片ID", max_length=255, null=True, blank=True)
    title_photo_id = models.CharField(db_column="title_photo_id", verbose_name="活动内顶部图片ID", max_length=255, null=True, blank=True)
    status = models.CharField(db_column="status", verbose_name="数据状态", default="normal", max_length=255)
    create_time = models.IntegerField(db_column="create_time", verbose_name="活动创建时间", default=int(time.time()))


    class Meta:
        db_table = "campaigns"
    

    @classmethod
    def get_all_location_list(cls):
        data = cls.objects.filter(status='normal').values('location').annotate(c=Count('location'))
        data = list(data)
        return data
    
    @classmethod
    def get_campaigns_selecet_all(cls):
        data_list = list()
        data = cls.objects.values('location').annotate(c=Count('location'))
        for i in data:
            o = cls.objects.filter(location=i['location']).values("campaign_id", "campaign_name")
            for j in o:
                j['campaign_name'] = i['location'] + '__' + j['campaign_name']
            data_list.extend(o)
        return data_list

def create_model_data(model, data):
    return model.objects.create(**data)

def update_models_by_pk(model, pk, data):
    model.objects.filter(pk=pk).update(**data)

def get_data_list(model, current_page, search_value=None, order_by="-pk", search_value_type='dict'):
    if search_value:
        if search_value_type == 'dict':
            data_list = model.objects.filter(**search_value, status='normal'). \
                order_by(order_by)
        else:
            data_list = model.objects.filter(search_value, status='normal'). \
                order_by(order_by)
    else:
        data_list = model.objects.filter(status='normal'). \
            order_by(order_by)
    p = Paginator(data_list, 15)
    return p.page(current_page).object_list.values()

def get_data_count(model, search_value=None, search_value_type='dict'):
    if search_value:
        if search_value_type == 'dict':
            count = model.objects.filter(**search_value, status='normal').count()
        else:
            count = model.objects.filter(search_value, status='normal').count()
    else:
        count = model.objects.filter(status='normal').count()
    return count

def get_model_obj_by_pk(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None