# Generated by Django 4.2.4 on 2023-09-11 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("imdb_api", "0011_alter_movie_vote_average"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrailerVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("key", models.CharField(max_length=255)),
                ("site", models.CharField(max_length=255)),
                ("size", models.IntegerField()),
                ("type", models.CharField(max_length=255)),
                ("official", models.BooleanField()),
                ("published_at", models.DateTimeField()),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="imdb_api.movie"
                    ),
                ),
            ],
        ),
    ]