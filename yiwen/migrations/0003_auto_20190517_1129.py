# Generated by Django 2.2.1 on 2019-05-17 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yiwen', '0002_question_typeofquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.CharField(max_length=250),
        ),
    ]
