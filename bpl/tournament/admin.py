import csv

from django.contrib import admin
from django.http import HttpResponse

from . import models


class BaseAdmin(admin.ModelAdmin):
    list_display = ("last_updated",)
    actions = ["export_as_csv"]

    @admin.action(description="Export Selected as CSV")
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            _ = writer.writerow([getattr(obj, field) for field in field_names])

        return response


class TournamentAdmin(BaseAdmin):
    list_display = ("tournament",)


class LeagueAdmin(BaseAdmin):
    list_display = ("league",)


class FranchiseAdmin(BaseAdmin):
    list_display = (
        "franchise",
        "user",
    )


class PlayerAdmin(BaseAdmin):
    list_display = ("player_name", "price", "franchise", "league", "tournament")
    list_filter = ("franchise", "league", "tournament")
    list_per_page = 100


class FixtureAdmin(BaseAdmin):
    list_display = (
        "match_number",
        "scorecard_url",
        "match_date",
        "tournament",
    )
    list_filter = ("match_number", "match_date", "tournament")


class MatchPointAdmin(BaseAdmin):
    list_display = (
        "match_name",
        "match_date",
        "player_name",
        "batting_points",
        "bowling_points",
        "fielding_points",
        "pom_points",
        "total_points",
    )
    list_filter = ("match_name", "match_date", "player_name")


class ScoreAdmin(BaseAdmin):
    list_display = (
        "match_name",
        "player_name",
        "power_player",
        "score",
        "franchise",
        "league",
        "tournament",
    )
    list_filter = ("match_name", "player_name", "franchise", "league", "tournament")


class StandingAdmin(BaseAdmin):
    list_display = ("tournament", "league", "franchise", "points")
    list_filter = ("franchise", "league", "tournament")


admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.League, LeagueAdmin)
admin.site.register(models.Franchise, FranchiseAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Fixture, FixtureAdmin)
admin.site.register(models.MatchPoint, MatchPointAdmin)
admin.site.register(models.Score, ScoreAdmin)
admin.site.register(models.Standing, StandingAdmin)
