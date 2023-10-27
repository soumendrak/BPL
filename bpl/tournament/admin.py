from django.contrib import admin

from . import models


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("tournament",)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ("league",)


class FranchiseAdmin(admin.ModelAdmin):
    list_display = (
        "franchise",
        "user",
    )


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("player_name", "price", "last_updated")


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "match_number",
        "match_name",
        "match_date",
        "player_name",
        "batting_points",
        "bowling_points",
        "fielding_points",
        "pom_points",
        "total_points",
        "last_updated",
    )
    list_filter = ("match_number", "match_name", "match_date", "player_name")


class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "match_number",
        "player_name",
        "power_player",
        "score",
        "franchise",
        "league",
        "tournament",
        "last_updated",
    )
    list_filter = ("match_number", "player_name", "franchise", "league", "tournament")


class StandingAdmin(admin.ModelAdmin):
    list_display = ("tournament", "league", "franchise", "points", "last_updated")
    list_filter = ("franchise", "league", "tournament")


admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.League, LeagueAdmin)
admin.site.register(models.Franchise, FranchiseAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Score, ScoreAdmin)
admin.site.register(models.Standing, StandingAdmin)
