# Generated by Django 3.2.13 on 2022-06-01 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_articles'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Articles',
        ),
    ]