# Generated by Django 2.2 on 2019-05-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190506_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('男', '男'), ('女', '女')], default='男', help_text='性别', max_length=6, verbose_name='性别'),
        ),
    ]
