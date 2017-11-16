from django.db import models
from db.base import BaseModel
from tinymce.models import HTMLField


class GoodType(BaseModel):
    name = models.CharField(max_length=20, verbose_name='商品名称')

    image = models.ImageField(upload_to='type', verbose_name='商品图片')

    logo = models.CharField(max_length=20, verbose_name='标识')

    class Meta:
        db_table = 'tt_goods_type'
        verbose_name = '商品种类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodSku(BaseModel):
    """
    商品的SKU表
    
    """
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    type = models.ForeignKey('GoodType', verbose_name='商品种类')
    goods = models.ForeignKey('GoodSPU', verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    danwei = models.CharField(max_length=20, verbose_name='商品单位')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='商品状态')
    image = models.ImageField(upload_to='goods', verbose_name=  '商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')

    class Meta:
        db_table = 'tt_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class GoodSPU(BaseModel):
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'tt_goods_spu'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


class GoodImage(BaseModel):
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')
    sku = models.ForeignKey('GoodSku', verbose_name='商品')

    class Meta:
        db_table = 'tt_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class IndexTaketurns(BaseModel):
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    sku = models.ForeignKey('GoodSku', verbose_name='商品')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'tt_taketurns'
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name


class IndexActivity(BaseModel):
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    url = models.URLField(verbose_name='活动链接')

    class Meta:
        db_table = 'tt_activity'
        verbose_name = '首页活动展示图'
        verbose_name_plural = verbose_name


class GoodIfication(BaseModel):
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    sku = models.ForeignKey('GoodSku', verbose_name='商品SKU')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    type = models.ForeignKey('GoodType', verbose_name='商品种类')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示标识')

    class Meta:
        db_table = 'tt_goods_ification'
        verbose_name = '商品分类展示表'
        verbose_name_plural = verbose_name
