# Generated by Django 4.2.6 on 2023-10-29 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Franchise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("franchise", models.CharField(max_length=100, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        to_field="username",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="League",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("league", models.CharField(max_length=100, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MatchPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("match_name", models.CharField(max_length=100, unique=True)),
                ("match_date", models.DateField()),
                ("batting_points", models.IntegerField()),
                ("bowling_points", models.IntegerField()),
                ("fielding_points", models.IntegerField()),
                ("pom_points", models.IntegerField()),
                ("total_points", models.IntegerField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Matches",
                "ordering": ["match_date"],
            },
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("player_name", models.CharField(max_length=100, unique=True)),
                ("price", models.IntegerField(default=10)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tournament", models.CharField(max_length=100, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Standing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("points", models.IntegerField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "franchise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.franchise", to_field="franchise"
                    ),
                ),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.league", to_field="league"
                    ),
                ),
                (
                    "tournament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.tournament", to_field="tournament"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Standings",
                "ordering": ["points"],
            },
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("power_player", models.BooleanField(default=False)),
                ("score", models.IntegerField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "franchise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.franchise", to_field="franchise"
                    ),
                ),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.league", to_field="league"
                    ),
                ),
                (
                    "match_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.matchpoint", to_field="match_name"
                    ),
                ),
                (
                    "player_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.player", to_field="player_name"
                    ),
                ),
                (
                    "tournament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.tournament", to_field="tournament"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="matchpoint",
            name="player_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tournament.player", to_field="player_name"
            ),
        ),
        migrations.AddField(
            model_name="matchpoint",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tournament.tournament", to_field="tournament"
            ),
        ),
        migrations.CreateModel(
            name="Fixture",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("scorecard_url", models.URLField(max_length=300, unique=True)),
                ("match_number", models.IntegerField()),
                ("match_date", models.DateField()),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "tournament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tournament.tournament", to_field="tournament"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Fixtures",
                "ordering": ["match_number"],
            },
        ),
    ]