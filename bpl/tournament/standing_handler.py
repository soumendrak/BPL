import pandas as pd
from dateutil.utils import today

from .models import MatchPoint, Standing


def fetch_standings(request) -> pd.DataFrame:
    standing_df = pd.DataFrame.from_records(Standing.objects.all().values())
    # if standing_df["prev_points_updated_date"] < (today() - pd.Timedelta(days=1)):
    #     standing_df["previous_points"] = standing_df["points"]
    #     standing_df["prev_points_updated_date"] += today() - pd.Timedelta(days=1)
    match_point_df = pd.DataFrame.from_records(MatchPoint.objects.filter(match_date=today()).values())
    new_df = (
        match_point_df.groupby(by=["tournament_id", "league_id", "franchise_id"])["total_points"]
        .sum()
        .to_frame("total_points")
        .reset_index()
    )
    standing_df = pd.merge(standing_df, new_df, on=["tournament_id", "league_id", "franchise_id"], how="left")
    standing_df["total_points"].fillna(0, inplace=True)
    standing_df["points"] += standing_df["total_points"]
    standing_df.drop(
        columns=["id", "tournament_id", "league_id", "created", "last_updated", "total_points"], inplace=True
    )
    standing_df = standing_df.sort_values(by="points", ascending=False)
    # for index, row in standing_df.iterrows():
    #     Standing.objects.update_or_create(
    #         tournament_id=row["tournament_id"],
    #         league_id=row["league_id"],
    #         franchise_id=row["franchise_id"],
    #         defaults={
    #             "points": row["points"],
    #             "previous_points": row["previous_points"],
    #             "prev_points_updated_date": row["prev_points_updated_date"]
    #         }
    #     )
    return standing_df
