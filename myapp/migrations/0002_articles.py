# Generated by Django 4.0.4 on 2022-05-31 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_img_url', models.URLField()),
                ('article_author', models.CharField(max_length=50)),
                ('article_title', models.CharField(max_length=100)),
                ('article_description', models.CharField(max_length=500)),
                ('article_url', models.URLField()),
                ('article_publish', models.DateTimeField()),
                ('article_category', models.CharField(max_length=50)),
            ],
        ),
    ]
