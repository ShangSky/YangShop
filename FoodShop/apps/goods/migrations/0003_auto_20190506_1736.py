# Generated by Django 2.2 on 2019-05-06 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190502_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='rate',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, verbose_name='评分'),
        ),
    ]
