# Generated by Django 2.2.3 on 2019-08-03 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionsetting',
            name='check_cookie',
            field=models.BooleanField(default=False, help_text='检查COOKIE'),
        ),
    ]
