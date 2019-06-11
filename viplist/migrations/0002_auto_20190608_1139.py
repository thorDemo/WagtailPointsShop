# Generated by Django 2.2.1 on 2019-06-08 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viplist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VipSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_valid', models.IntegerField(help_text='VIP客户积分有效期限 单位月')),
                ('common_valid', models.IntegerField(help_text='普通客户积分有效期限 单位月')),
                ('update_time', models.TimeField(auto_now=True)),
            ],
            options={
                'db_table': 'vip_setting',
            },
        ),
        migrations.AddField(
            model_name='viplist',
            name='update_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
