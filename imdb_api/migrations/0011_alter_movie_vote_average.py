# Generated by Django 4.2.4 on 2023-09-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("imdb_api", "0010_alter_movie_release_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="vote_average",
            field=models.FloatField(default=0.0),
        ),
    ]
