# Generated by Django 2.2.1 on 2019-06-12 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0008_auto_20190608_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add',
            name='change_points',
            field=models.IntegerField(help_text='流水加减 这里输入的是流水不是积分'),
        ),
        migrations.AlterField(
            model_name='add',
            name='update_time',
            field=models.DateField(help_text='积分修改时间'),
        ),
    ]
