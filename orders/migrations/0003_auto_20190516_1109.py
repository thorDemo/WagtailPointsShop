# Generated by Django 2.2.1 on 2019-05-16 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190516_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('0', '待确认'), ('1', '待发货'), ('2', '配送中'), ('3', '已送达'), ('4', '已取消')], default='0', max_length=255),
        ),
    ]
