# Generated by Django 2.1.7 on 2019-03-09 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d'),
        ),
    ]
