# Generated by Django 3.2.5 on 2021-08-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
