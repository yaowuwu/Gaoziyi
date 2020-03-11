import requests
import random

from django.core.cache import cache

from swiper import conf
from common import keys


def gen_randcode(length=6):
    '''产生一个指定长度的随机码'''
    start = 10 ** (length-1)
    end = 10 ** length - 1
    return str(random.randint(start, end))

def send_vcode(mobile):
    '''发送短信验证码'''
    # 防止用户重复发送验证码，先看缓存中有没有验证码，如果存在直接返回
    key = keys.VCODE_K % mobile
    if cache.get(key):
        return True
    else:
        args = conf.YZX_VCODE_ARGS.copy()
        args['mobile'] = mobile
        args['param'] = gen_randcode()
        print(args['param'])

        response = requests.post(conf.YZX_API, json=args)
        if response.status_code == 200:
            result = response.json()
            if result['msg'] == 'OK':
                cache.set(key, args['param'], 900)
                return True
        print(response.text)
        return False
