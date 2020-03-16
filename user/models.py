from django.db import models

# Create your models here.


class User(models.Model):
    GENDER = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('郑州', '郑州'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('成都', '成都'),
        ('沈阳', '沈阳'),


    )
    phonenum = models.CharField(max_length=15, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER, default='male', verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象的URL')
    location = models.CharField(max_length=10, verbose_name='常居地', choices=LOCATION, default='北京')

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    dating_location = models.CharField(max_length=10, choices=User.LOCATION, default='北京', verbose_name='目标城市')
    min_distance = models.IntegerField(max_length=64, verbose_name='最小查找范围', default=1)
    max_distance = models.IntegerField(max_length=64, verbose_name='最大查找范围', default=60)
    min_dating_age = models.IntegerField(verbose_name='最小交友年龄', default=16)
    max_dating_age = models.IntegerField(verbose_name='最大交友年龄', default=80)
    dating_gender = models.CharField(max_length=10, choices=User.GENDER, default='female', verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=False, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    def to_dict(self):
        return {
            'id': self.id,
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }