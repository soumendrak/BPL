from datetime import datetime, timedelta

from .models import Fixture, Franchise, Player
from .score_computation import Batting, Bowling, read_webpage


def get_scorecard_url() -> list[str]:
    # Read `scorecard_url` column from fixture table and call read_webpage function
    yesterday = datetime.now() - timedelta(days=1)
    fixtures = Fixture.objects.filter(match_date=yesterday)
    _scorecard_urls: list[str] = [fixture.scorecard_url for fixture in fixtures]
    return _scorecard_urls


def scorecard_url_to_score(scorecard_urls: list[str]):
    # Call read_webpage function
    for scorecard_url in scorecard_urls:
        try:
            dfs = read_webpage(scorecard_url)
            first_batting = Batting(dfs[0])
            first_batting.batting_preprocessing()
            first_batting_df = first_batting.batting_score_calculation()
            first_bowling = Bowling(dfs[1])
            first_bowling.bowling_preprocessing()
            first_bowling_df = first_bowling.bowling_score_calculation()
            second_batting = Batting(dfs[2])
            second_batting.batting_preprocessing()
            second_batting_df = second_batting.batting_score_calculation()
            second_bowling = Bowling(dfs[3])
            second_bowling.bowling_preprocessing()
            second_bowling_df = second_bowling.bowling_score_calculation()
            print(first_batting_df, "\n", first_bowling_df, "\n", second_batting_df, "\n", second_bowling_df)
            return first_batting_df, first_bowling_df, second_batting_df, second_bowling_df
        except Exception as e:
            print(e)
            continue


def fetch_players():
    # Read `player_name` column from player table
    return Player.objects.all()


def get_franchise(request):
    # Read `franchise` column from franchise table
    return Franchise.objects.filter(user=request.user)


if __name__ == "__main__":
    scorecard_urls = get_scorecard_url()
    scorecard_url_to_score(scorecard_urls)
