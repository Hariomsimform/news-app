# Generated by Django 3.2.13 on 2022-06-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_userprofile_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='article_author',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AlterField(
            model_name='articles',
            name='article_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='articles',
            name='article_title',
            field=models.TextField(),
        ),
    ]
