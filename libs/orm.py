import logging
import datetime

from django.db import models
from django.db.models import query
from libs.cache import rds
from common import keys


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    '''
    Save the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    :param self:
    :param force_insert:
    :param force_update:
    :param using:
    :param update_fields:
    :return:
    '''
    # 调用原 save() 方法将数据保存到数据库中
    self._save(force_insert, force_update, using, update_fields)
    # 将model_obj 数据缓存在rds中
    model_key = keys.MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(model_key, self, 86400 * 7)
    print(rds.keys())


def get(self, *args, **kwargs):
    """
        Perform the query and return a single object matching the given
        keyword arguments.
    """
    # 取出 model 的名称
    cls_name = self.model.__name__

    # 检查kwargs中是否有id 或 pk
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk is not None:
        model_key = keys.MODEL_K % (cls_name, pk)  # 定义缓存中的key
        model_obj = rds.get(model_key)  # 从redis中取出缓存对象
        if isinstance(model_obj, self.model):
            return model_obj
    # 如果缓存中没有取到model 数据， 直接从数据库中获取
    model_obj = self._get(*args, **kwargs)
    # 将取到的model对象保存到redis中
    model_key = keys.MODEL_K % (cls_name, model_obj.pk)
    rds.set(model_key, model_obj, 86400 * 7)
    print(rds.keys())
    return model_obj


def to_dict(self, exclude=()):
    '''将当前模型转换为 dict 类型'''
    attr_dict = {}
    # 需要强制转换成字符串类型
    force_str_types = (datetime.datetime, datetime.date, datetime.time)
    for field in self._meta.fields:
        name = field.attname
        value = getattr(self, name)
        if name not in exclude:
            #   将特色类型强转成 str 类型
            if isinstance(value, force_str_types):
                value = str(value)
            attr_dict[name] = value
    return attr_dict


def patch_model():
    ''' 通过 Monkey Patch 的方式为 DjangoORM 增加缓存处理 '''
    # 修改save的方法
    models.Model._save = models.Model.save
    models.Model.save = save

    # 修改get方法
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model.to_dict = to_dict