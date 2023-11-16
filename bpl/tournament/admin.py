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
    list_display = ("tournament_name",)


class LeagueAdmin(BaseAdmin):
    list_display = ("league_name",)


class FranchiseAdmin(BaseAdmin):
    list_display = ("franchise_name",)


class PlayerProfileAdmin(BaseAdmin):
    list_display = (
        "player_name",
        "country",
        "player_role",
        "profile_link",
    )


class FixtureAdmin(BaseAdmin):
    list_display = (
        "scorecard_url",
        "match_date",
        "tournament_name",
    )
    list_filter = ("match_date", "tournament_name")


class PlayerAdmin(BaseAdmin):
    list_display = ("player_name", "price", "franchise_name", "league_name", "tournament_name", "power_player")
    list_filter = ("franchise_name", "league_name", "tournament_name", "power_player")
    list_per_page = 50
    search_fields = ("player_name",)


class MatchPointAdmin(BaseAdmin):
    list_display = (
        "league_name",
        "franchise_name",
        "match_date",
        "player_name",
        "batting_points",
        "bowling_points",
        "fielding_points",
        "total_points",
    )
    list_filter = (
        "match_date",
        "player_name",
        "league_name",
        "franchise_name",
        "tournament_name",
    )


class StandingAdmin(BaseAdmin):
    list_display = ("tournament_name", "league_name", "franchise_name", "points")
    list_filter = ("franchise_name", "league_name", "tournament_name")


admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.League, LeagueAdmin)
admin.site.register(models.Franchise, FranchiseAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Fixture, FixtureAdmin)
admin.site.register(models.MatchPoint, MatchPointAdmin)
admin.site.register(models.Standing, StandingAdmin)
admin.site.register(models.PlayerProfile, PlayerProfileAdmin)
