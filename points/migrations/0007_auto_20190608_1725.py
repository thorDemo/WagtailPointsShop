# Generated by Django 2.2.1 on 2019-06-08 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0006_auto_20190516_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='points',
            old_name='month_water',
            new_name='one_month_capital_flow',
        ),
        migrations.RenameField(
            model_name='points',
            old_name='all_water',
            new_name='one_year_capital_flow',
        ),
    ]
