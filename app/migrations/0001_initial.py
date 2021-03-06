# Generated by Django 3.2.6 on 2021-08-31 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id_link', models.IntegerField(primary_key=True, serialize=False)),
                ('short_link', models.SlugField(max_length=6)),
                ('original_url', models.URLField(max_length=300)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
