# Generated by Django 2.2.1 on 2019-05-16 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('mulu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodssortpage',
            name='home_image',
            field=models.ForeignKey(blank=True, help_text='首页封面图片', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
