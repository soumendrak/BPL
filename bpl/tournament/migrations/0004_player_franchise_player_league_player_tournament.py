# Generated by Django 4.2.6 on 2023-11-01 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tournament", "0003_alter_franchise_options_alter_league_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="franchise",
            field=models.ForeignKey(
                default="Ahmdabad Cyanides",
                on_delete=django.db.models.deletion.CASCADE,
                to="tournament.franchise",
                to_field="franchise",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="player",
            name="league",
            field=models.ForeignKey(
                default="Banaas Premier League",
                on_delete=django.db.models.deletion.CASCADE,
                to="tournament.league",
                to_field="league",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="player",
            name="tournament",
            field=models.ForeignKey(
                default="ODIWC2023",
                on_delete=django.db.models.deletion.CASCADE,
                to="tournament.tournament",
                to_field="tournament",
            ),
            preserve_default=False,
        ),
    ]