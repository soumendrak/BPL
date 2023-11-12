from django.db import models

from config.settings.base import AUTH_USER_MODEL


class Tournament(models.Model):
    """
    This will be handled by only the super admin
    """

    tournament = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tournament

    class Meta:
        verbose_name_plural = "Tournaments"


class League(models.Model):
    # This will be handled by admin league
    league = models.CharField(max_length=100, unique=True)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.league

    class Meta:
        verbose_name_plural = "Leagues"
        ordering = ["league"]


class Franchise(models.Model):
    # This will be handled by individual user
    franchise = models.CharField(max_length=100, unique=True)
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.franchise

    class Meta:
        verbose_name_plural = "Franchises"
        ordering = ["franchise"]


class Player(models.Model):
    player_name = models.CharField(max_length=100, unique=True)
    franchise = models.ForeignKey(Franchise, to_field="franchise", on_delete=models.CASCADE)
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    power_player = models.BooleanField(default=False)
    price = models.IntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name_plural = "Players"
        ordering = ["player_name"]


class Fixture(models.Model):
    scorecard_url = models.URLField(max_length=300, unique=True)
    match_number = models.IntegerField()
    match_date = models.DateField()
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tournament) + " - " + str(self.match_number) + " - " + str(self.match_date)

    class Meta:
        verbose_name_plural = "Fixtures"
        ordering = ["match_number"]


class MatchPoint(models.Model):
    match_name = models.CharField(max_length=100)
    match_date = models.DateField()
    player_name = models.ForeignKey(Player, to_field="player_name", on_delete=models.CASCADE)
    batting_points = models.IntegerField()
    bowling_points = models.IntegerField()
    fielding_points = models.IntegerField()
    pom_points = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField()
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE, default="Banaas Premier League")
    franchise = models.ForeignKey(Franchise, to_field="franchise", on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.league) + " - " + str(self.match_name) + " - " + str(self.match_date)

    class Meta:
        verbose_name_plural = "Matches"
        ordering = ["match_date", "total_points"]
        unique_together = ("player_name", "match_date", "league")


class Score(models.Model):
    match_name = models.CharField(max_length=100)
    score = models.IntegerField(null=True, blank=True, default=0)
    player_name = models.ForeignKey(Player, to_field="player_name", on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, to_field="franchise", on_delete=models.CASCADE)
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.franchise) + " - " + str(self.player_name)

    class Meta:
        verbose_name_plural = "Scores"
        ordering = ["score"]


class Standing(models.Model):
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, to_field="franchise", on_delete=models.CASCADE)
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.franchise

    class Meta:
        verbose_name_plural = "Standings"
        ordering = ["points"]
