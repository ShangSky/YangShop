# Generated by Django 2.2 on 2019-05-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190430_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergoods',
            name='content',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='评论内容'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='评分'),
        ),
    ]
