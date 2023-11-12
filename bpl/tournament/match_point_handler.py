import logging
from datetime import datetime, timedelta
from functools import lru_cache

import pandas as pd
from dateutil.utils import today

from .models import Fixture, Franchise, League, MatchPoint, Player, Tournament
from .score_computation import Batting, Bowling, read_webpage

yesterday = datetime.now() - timedelta(days=1)


@lru_cache(maxsize=32)
def get_scorecard_url() -> list[str]:
    # Read `scorecard_url` column from fixture table and call read_webpage function
    fixtures = Fixture.objects.filter(match_date=today())
    _scorecard_urls: list[str] = [fixture.scorecard_url for fixture in fixtures]
    logging.info(f"{_scorecard_urls=}")
    return _scorecard_urls


def scorecard_url_to_score(scorecard_urls: list[str]) -> list[list[pd.DataFrame]]:
    # Call read_webpage function
    logging.info(f"{scorecard_urls=}")
    matches = []
    for count, scorecard_url in enumerate(scorecard_urls):
        try:
            dfs = read_webpage(scorecard_url)
            logging.info(f"{len(dfs)=}")
            first_batting = Batting(dfs[0])
            first_batting.batting_preprocessing()
            first_batting_df = first_batting.batting_score_calculation()
            first_bowling = Bowling(dfs[1])
            first_bowling.bowling_preprocessing()
            first_bowling_df = first_bowling.bowling_score_calculation()
            if len(dfs) > 8:
                second_batting = Batting(dfs[2])
                second_batting.batting_preprocessing()
                second_batting_df = second_batting.batting_score_calculation()
                second_bowling = Bowling(dfs[3])
                second_bowling.bowling_preprocessing()
                second_bowling_df = second_bowling.bowling_score_calculation()
            else:
                second_batting_df = pd.DataFrame()
                second_bowling_df = pd.DataFrame()
            matches.append([first_batting_df, first_bowling_df, second_batting_df, second_bowling_df])
            print(first_batting_df, "\n", first_bowling_df, "\n", second_batting_df, "\n", second_bowling_df)
        except Exception as e:
            print(e)
            continue
    print(matches)
    return matches


@lru_cache(maxsize=32)
def fetch_players() -> pd.DataFrame:
    # Read `player_name` column from player table
    return pd.DataFrame.from_records(Player.objects.all().values())


def prepare_final_match_point_df(request) -> None:
    merged_df = fetch_players()
    match_scorecards = scorecard_url_to_score(get_scorecard_url())
    for match_scorecard in match_scorecards:
        # Iterates over each match scorecard
        batting_df = pd.concat([match_scorecard[0], match_scorecard[2]], ignore_index=True)
        bowling_df = pd.concat([match_scorecard[1], match_scorecard[3]], ignore_index=True)
        merged_df = pd.merge(merged_df, batting_df, how="outer", left_on="player_name", right_on="BATTING")
        merged_df = pd.merge(merged_df, bowling_df, how="outer", left_on="player_name", right_on="BOWLING")
        merged_df = merged_df.dropna(subset=["Total Batting", "Total Bowling"], how="all").reset_index(drop=True)
        merged_df = merged_df.dropna(subset=["player_name"], how="all").reset_index(drop=True)  # TODO
        merged_df.fillna({"Total Bowling": 0, "Total Batting": 0, "Total Fielding": 0}, inplace=True)
        for index, row in merged_df.iterrows():
            match_point_model = MatchPoint()
            match_point_model.match_name = "default"  # TODO: Add match name
            match_point_model.match_date = today()
            match_point_model.league = League.objects.get(league="Banaas Premier League")  # TODO: Make Dynamic
            match_point_model.tournament = Tournament.objects.get(tournament="ODIWC2023")  # TODO: Make Dynamic
            match_point_model.player_name = Player.objects.get(player_name=row["player_name"])
            match_point_model.franchise = Franchise.objects.get(franchise=row["franchise_id"])
            match_point_model.batting_points = row["Total Batting"] if "Total Batting" in merged_df.columns else 0
            match_point_model.bowling_points = row["Total Bowling"] if "Total Bowling" in merged_df.columns else 0
            match_point_model.fielding_points = row["Total Fielding"] if "Total Fielding" in merged_df.columns else 0
            match_point_model.pom_points = 0  # TODO: Add pom points
            match_point_model.total_points = (
                match_point_model.batting_points + match_point_model.bowling_points + match_point_model.fielding_points
            )
            # match_point_model.save()
            match_point, created = MatchPoint.objects.update_or_create(
                match_date=match_point_model.match_date,
                player_name=match_point_model.player_name,
                league=match_point_model.league,
                defaults={
                    "match_name": match_point_model.match_name,
                    "batting_points": match_point_model.batting_points,
                    "bowling_points": match_point_model.bowling_points,
                    "fielding_points": match_point_model.fielding_points,
                    "pom_points": match_point_model.pom_points,
                    "total_points": match_point_model.total_points,
                    "franchise": match_point_model.franchise,
                    "tournament": match_point_model.tournament,
                },
            )


# if __name__ == "__main__":
#     scorecard_urls = get_scorecard_url()
#     scorecard_url_to_score(scorecard_urls)
