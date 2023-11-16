from django.db import models
from django.utils import timezone


class Tournament(models.Model):
    """
    This will be handled by only the super admin
    """

    tournament_name = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.tournament_name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.tournament_name=}>"

    class Meta:
        verbose_name_plural = "Tournaments"


class League(models.Model):
    # This will be handled by admin league_name
    league_name = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.league_name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.league_name=}>"

    class Meta:
        verbose_name_plural = "Leagues"
        ordering = ["league_name"]


class Franchise(models.Model):
    # This will be handled by individual user
    franchise_name = models.CharField(max_length=100, primary_key=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.franchise_name)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.franchise_name=}>"

    class Meta:
        verbose_name_plural = "Franchises"
        ordering = ["franchise_name"]


class PlayerProfile(models.Model):
    player_name = models.CharField(max_length=100, primary_key=True)
    profile_link = models.URLField(max_length=300, unique=True, blank=True, null=True, default=None)
    country = models.CharField(max_length=100, blank=True, null=True, default=None)
    player_role = models.CharField(max_length=100, blank=True, null=True, default=None)  # TODO: Make it a choice field
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.player_name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.player_name=} {self.country=} {self.player_role=}>"

    class Meta:
        verbose_name_plural = "Player Profiles"
        ordering = ["player_name"]


class Fixture(models.Model):
    scorecard_url = models.URLField(max_length=300, primary_key=True)
    match_date = models.DateField()
    tournament_name = models.ForeignKey(Tournament, to_field="tournament_name", on_delete=models.CASCADE)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.tournament_name) + " - " + str(self.match_date)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.tournament_name=} {self.match_date=}>"

    class Meta:
        verbose_name_plural = "Fixtures"
        ordering = ["match_date"]


class Player(models.Model):
    player_name = models.ForeignKey(PlayerProfile, to_field="player_name", on_delete=models.CASCADE)
    franchise_name = models.ForeignKey(Franchise, to_field="franchise_name", on_delete=models.CASCADE)
    league_name = models.ForeignKey(League, to_field="league_name", on_delete=models.CASCADE)
    tournament_name = models.ForeignKey(Tournament, to_field="tournament_name", on_delete=models.CASCADE)
    power_player = models.BooleanField(default=False)
    price = models.IntegerField(default=10)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.player_name

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.player_name=} {self.franchise_name=} {self.league_name=} "
            f"{self.tournament_name=} {self.power_player=} {self.price=}>"
        )

    class Meta:
        verbose_name_plural = "Players"
        ordering = ["player_name"]
        unique_together = ("player_name", "franchise_name", "league_name", "tournament_name")


class MatchPoint(models.Model):
    match_date = models.DateField()
    player_name = models.ForeignKey(PlayerProfile, to_field="player_name", on_delete=models.CASCADE)
    batting_points = models.IntegerField()
    bowling_points = models.IntegerField()
    fielding_points = models.IntegerField()
    pom_points = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField()
    league_name = models.ForeignKey(
        League, to_field="league_name", on_delete=models.CASCADE, default="Banaas Premier League"
    )
    franchise_name = models.ForeignKey(Franchise, to_field="franchise_name", on_delete=models.CASCADE)
    tournament_name = models.ForeignKey(Tournament, to_field="tournament_name", on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.league_name) + " - " + str(self.match_date)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.player_name=} {self.franchise_name=} {self.league_name=} "
            f"{self.tournament_name=} {self.match_date=}>"
        )

    class Meta:
        verbose_name_plural = "MatchPoints"
        ordering = ["match_date", "total_points"]
        unique_together = ("player_name", "match_date", "league_name")


class Standing(models.Model):
    tournament_name = models.ForeignKey(Tournament, to_field="tournament_name", on_delete=models.CASCADE)
    league_name = models.ForeignKey(League, to_field="league_name", on_delete=models.CASCADE)
    franchise_name = models.ForeignKey(Franchise, to_field="franchise_name", on_delete=models.CASCADE)
    points = models.IntegerField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    last_updated = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.franchise_name) + " - " + str(self.league_name) + " - " + str(self.tournament_name)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.franchise_name=} {self.league_name=} {self.tournament_name=} "
            f"{self.points=}>"
        )

    class Meta:
        verbose_name_plural = "Standings"
        ordering = ["points"]
        unique_together = ("tournament_name", "league_name", "franchise_name")
