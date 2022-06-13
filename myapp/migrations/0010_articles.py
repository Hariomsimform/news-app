# Generated by Django 3.2.13 on 2022-06-02 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_delete_articles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_img_url', models.URLField()),
                ('article_author', models.CharField(max_length=150)),
                ('article_title', models.CharField(max_length=150)),
                ('article_description', models.TextField(max_length=800)),
                ('article_url', models.URLField()),
                ('article_publish', models.DateTimeField()),
                ('article_category', models.CharField(max_length=50)),
            ],
        ),
    ]