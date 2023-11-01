from dateutil.utils import today

from .models import Fixture, Franchise, Player
from .score_computation import Batting, Bowling, read_webpage


def get_scorecard_url() -> list[str]:
    # Read `scorecard_url` column from fixture table and call read_webpage function
    fixtures = Fixture.objects.filter(match_date=today())
    scorecard_urls = [fixture.scorecard_url for fixture in fixtures]
    return scorecard_urls


def scorecard_url_to_score(scorecard_urls: list[str]):
    # Call read_webpage function
    for scorecard_url in scorecard_urls:
        try:
            dfs = read_webpage(scorecard_url)
            batting = Batting(dfs[0])
            batting.batting_preprocessing()
            batting_df = batting.batting_score_calculation()
            bowling = Bowling(dfs[1])
            bowling.bowling_preprocessing()
            bowling_df = bowling.bowling_score_calculation()
            return batting_df, bowling_df
        except Exception as e:
            print(e)
            continue


def fetch_players():
    # Read `player_name` column from player table
    return Player.objects.all()


def get_franchise(request):
    # Read `franchise` column from franchise table
    return Franchise.objects.filter(user=request.user)
