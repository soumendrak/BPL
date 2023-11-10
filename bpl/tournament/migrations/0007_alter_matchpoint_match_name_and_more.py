# Generated by Django 4.2.6 on 2023-11-10 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournament", "0006_alter_player_franchise_alter_player_league_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="matchpoint",
            name="match_name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="matchpoint",
            name="pom_points",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="score",
            name="match_name",
            field=models.CharField(max_length=100),
        ),
    ]
