from django.db import models
from db.base import BaseModel


class OrderInfo(BaseModel):

    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    user = models.ForeignKey('user.User',verbose_name='用户')
    pay_status = models.IntegerField(default=1,choices=PAY_METHOD_CHOICES,verbose_name='支付方式')
    order_status = models.IntegerField(default=1,choices=ORDER_STATUS_CHOICES,verbose_name='支付状态')
    time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    order_number = models.CharField(max_length=128,verbose_name='支付编号')
    order_id = models.CharField(max_length=128,primary_key=True,verbose_name='订单ID')
    total_count = models.IntegerField(default=1,verbose_name='总数目')
    total_money = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总金额')
    freight = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='运费')

    class Meta:
        db_table = 'tt_order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class GoodOrder(BaseModel):

    order = models.ForeignKey('OrderInfo',verbose_name='订单id')
    sku = models.ForeignKey('goods.GoodSku',verbose_name='sku_id')
    number = models.IntegerField(default=1,verbose_name='商品数量')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    comment= models.CharField(max_length=256,verbose_name='评论')

    class Meta:
        db_table = 'tt_order_goods'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name

