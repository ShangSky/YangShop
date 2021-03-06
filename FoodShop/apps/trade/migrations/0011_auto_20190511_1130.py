# Generated by Django 2.2 on 2019-05-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0010_auto_20190509_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'ordering': ('-create_time',), 'verbose_name': '订单', 'verbose_name_plural': '订单'},
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('WAIT_BUYER_PAY', '交易创建'), ('TRADE_CLOSED', '超时关闭'), ('TRADE_SUCCESS', '支付成功'), ('TRADE_FINISHED', '交易接收')], default='WAIT_BUYER_PAY', max_length=30, verbose_name='交易状态'),
        ),
    ]
