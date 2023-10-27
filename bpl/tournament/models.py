from django.db import models

from config.settings.base import AUTH_USER_MODEL


class Tournament(models.Model):
    """
    Tournament 1 <> N Leagues
    League 1 <> N Franchises
    Franchise 1 <> N Players
    Player 1 <> N Matches
    This will be handled by only the super admin
    """

    tournament = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tournament


class League(models.Model):
    # This will be handled by admin league
    league = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.league


class Franchise(models.Model):
    # This will be handled by individual user
    franchise = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, to_field="username", on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.franchise


class Player(models.Model):
    player_name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player_name


class Match(models.Model):
    match_number = models.IntegerField(unique=True)
    match_name = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    player_name = models.ForeignKey(Player, to_field="player_name", on_delete=models.CASCADE)
    batting_points = models.IntegerField()
    bowling_points = models.IntegerField()
    fielding_points = models.IntegerField()
    pom_points = models.IntegerField()
    total_points = models.IntegerField()
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.match_number) + " - " + str(self.match_number) + str(self.match_date)

    class Meta:
        verbose_name_plural = "Matches"
        ordering = ["match_number"]


class Score(models.Model):
    match_number = models.ForeignKey(Match, to_field="match_number", on_delete=models.CASCADE)
    player_name = models.ForeignKey(Player, to_field="player_name", on_delete=models.CASCADE)
    power_player = models.BooleanField(default=False)
    score = models.IntegerField()
    franchise = models.ForeignKey(Franchise, to_field="franchise", on_delete=models.CASCADE)
    league = models.ForeignKey(League, to_field="league", on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, to_field="tournament", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.franchise) + " - " + str(self.player_name)


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
