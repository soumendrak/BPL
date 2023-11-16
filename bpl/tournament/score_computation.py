import logging
from dataclasses import dataclass

import pandas as pd

pd.options.mode.chained_assignment = None


def read_webpage(page_url: str) -> list[pd.DataFrame]:
    return pd.read_html(page_url)


@dataclass
class Batting:
    batting_df: pd.DataFrame = None

    @classmethod
    def individual_batting(cls, runs: int, fours: int, sixes: int, incident: str) -> int:
        if runs == 0 and incident != "not out":
            return -25
        else:
            return runs + (2 * fours) + (4 * sixes)

    @classmethod
    def sr_batting(cls, strike_rate: float) -> int:
        if strike_rate == 0:
            return -10
        elif 1 <= strike_rate <= 50:
            return -10
        elif 51 <= strike_rate <= 100:
            return 0
        elif 101 <= strike_rate <= 130:
            return 5
        elif 131 <= strike_rate <= 150:
            return 10
        elif 151 <= strike_rate <= 200:
            return 15
        elif 201 <= strike_rate <= 300:
            return 17
        elif 301 <= strike_rate <= 400:
            return 20
        elif 401 <= strike_rate <= 600:
            return 25

    @classmethod
    def bonus_batting(cls, runs: int) -> int:
        if runs <= 30:
            return 0
        elif 31 <= runs <= 50:
            return 5
        elif 51 <= runs <= 75:
            return 10
        elif 76 <= runs <= 100:
            return 15
        elif 101 <= runs <= 125:
            return 20
        elif 126 <= runs <= 150:
            return 25
        elif runs > 150:
            return 30
        else:
            print(f"invalid {runs=}")

    def batting_preprocessing(self):
        logging.info("Batting dataframe preprocessing started")
        try:
            column_mapping = {1: "Incident"}
            self.batting_df.rename(columns=column_mapping, inplace=True)
            self.batting_df = self.batting_df.dropna(how="all").reset_index(drop=True)
            # assign a column name to the unnamed column
            self.batting_df.rename(columns={self.batting_df.columns[1]: "Incident"}, inplace=True)
            # Delete the unnamed columns
            self.batting_df.drop(self.batting_df.filter(regex="Unname"), axis=1, inplace=True)
            # self.batting_df = self.batting_df.loc[:, ~self.batting_df.columns.str.contains("^Unnamed")]

            # Delete the last three rows
            # Get the index of the first occurrence of 'Extras' in the 'BATTING' column
            index = (self.batting_df["BATTING"] == "Extras").idxmax()
            # Select all rows up to (but not including) the row with 'Extras'
            self.batting_df = self.batting_df.iloc[:index]

            self.batting_df["Catch"] = self.batting_df["Incident"].str.extract(r"(?<=c\s)(.*)(?=\sb\s)")
            self.batting_df["Bowled"] = self.batting_df["Incident"].str.extract(r"(?<=\sb\s)(.*)")
            self.batting_df["Run Out"] = self.batting_df["Incident"].str.extract(r"(?<=run out \()(.*)(?=\))")
            self.batting_df["SR"] = self.batting_df["SR"].str.replace(r"-", "0")
            self.batting_df["BATTING"] = self.batting_df["BATTING"].str.replace(r"\(c\)|\†", "", regex=True)
            self.batting_df["BATTING"] = self.batting_df["BATTING"].str.strip()
        except Exception as e:
            logging.error(e)
        logging.info("Batting dataframe preprocessing completed")

    def batting_score_calculation(self) -> pd.DataFrame:
        # Calculate the points of the batsman by the following functions and add a column to the dataframe
        # individual_batting(runs: int, fours: int, sixes: int) -> int
        # sr_batting(strike_rate: int) -> int
        # bonus_batting(runs: int) -> int
        self.batting_df["Runs"] = self.batting_df["R"].astype(int, errors="ignore")
        self.batting_df["Fours"] = self.batting_df["4s"].astype(int, errors="ignore")
        self.batting_df["Sixes"] = self.batting_df["6s"].astype(int, errors="ignore")
        self.batting_df["Strike Rate"] = self.batting_df["SR"].astype(float, errors="ignore")

        self.batting_df["Individual Batting"] = self.batting_df.apply(
            lambda row: self.individual_batting(row["Runs"], row["Fours"], row["Sixes"], row["Incident"]), axis=1
        )
        self.batting_df["SR Batting"] = self.batting_df.apply(lambda row: self.sr_batting(row["Strike Rate"]), axis=1)
        self.batting_df["Bonus Batting"] = self.batting_df.apply(lambda row: self.bonus_batting(row["Runs"]), axis=1)

        self.batting_df["Total Batting"] = (
            self.batting_df["Individual Batting"] + self.batting_df["SR Batting"] + self.batting_df["Bonus Batting"]
        )

        # Drop following columns
        # R, 4s, 6s, SR
        self.batting_df.drop(columns=["R", "4s", "6s", "SR", "B", "M", "Fours", "Sixes", "Strike Rate"], inplace=True)
        self.batting_df.drop(columns=["Incident", "Catch", "Bowled", "Run Out"], inplace=True)
        self.batting_df.reset_index(drop=True, inplace=True)
        logging.info("Batting score calculation completed")
        return self.batting_df


def get_player_of_the_match(pom_df) -> str:
    try:
        pom = pom_df.loc[pom_df[0] == "Player Of The Match"][1]
        pom = pom.to_string(index=False)
        logging.info(f"{pom=}")
    except KeyError as e:
        pom = ""
        logging.info(f"{pom=} is not yet available due to {e}")
    return pom


@dataclass
class Bowling:
    bowling_df: pd.DataFrame = None

    @classmethod
    def maiden(cls, count: int) -> int:
        return 25 * count

    @classmethod
    def dot_ball(cls, count: int) -> int:
        return 2 * count

    @classmethod
    def wicket(cls, count: int) -> int:
        return 20 * count

    @classmethod
    def hattrick(cls, count: int) -> int:
        return 50 * count

    @classmethod
    def no_ball(cls, count: int) -> int:
        return -2 * count

    @classmethod
    def wide_ball(cls, count: int) -> int:
        return -1 * count

    @classmethod
    def bonus_bowling(cls, wickets: int) -> int:
        wickets_mapping = {
            0: 0,
            1: 0,
            2: 10,
            3: 20,
            4: 30,
            5: 40,
            6: 50,
            7: 60,
            8: 70,
            9: 80,
            10: 90,
        }
        return wickets_mapping[wickets]

    @classmethod
    def economy_bowling(cls, er: float) -> int:
        if er <= 3.99:
            return 25
        elif 4 <= er <= 5.99:
            return 15
        elif 6 <= er <= 7.99:
            return 5
        elif 8 <= er <= 9.99:
            return -7
        elif 10 <= er <= 11.99:
            return -12
        elif 12 <= er <= 14.99:
            return -15
        elif 15 <= er <= 17.99:
            return -20
        elif 18 <= er <= 19.99:
            return -25
        elif er > 20:
            return -30
        else:
            print(f"Invalid {er=}")

    def bowling_preprocessing(self):
        self.bowling_df = self.bowling_df[pd.to_numeric(self.bowling_df["O"], errors="coerce").notnull()]
        # Calculate the points of Bowler by the following functions and add a column to the dataframe
        # individual_bowling(item: str, count: int) -> int
        # bonus_bowling(wickets: int) -> int
        # economy_bowling(er: float) -> int
        self.bowling_df.loc[:, "M"] = self.bowling_df["M"].astype(int, errors="ignore")
        self.bowling_df.loc[:, "0s"] = self.bowling_df["0s"].astype(int, errors="ignore")
        self.bowling_df.loc[:, "W"] = self.bowling_df["W"].astype(int, errors="ignore")
        self.bowling_df.loc[:, "NB"] = self.bowling_df["NB"].astype(int, errors="ignore")
        self.bowling_df.loc[:, "WD"] = self.bowling_df["WD"].astype(int, errors="ignore")
        self.bowling_df.loc[:, "ECON"] = self.bowling_df["ECON"].astype(float, errors="ignore")

        logging.info("Bowling dataframe preprocessing completed")

        return self.bowling_df

    def bowling_score_calculation(self) -> pd.DataFrame:
        self.bowling_df.loc[:, "Maiden Points"] = self.bowling_df.apply(lambda row: self.maiden(row["M"]), axis=1)
        self.bowling_df.loc[:, "Dot Ball Points"] = self.bowling_df.apply(lambda row: self.dot_ball(row["0s"]), axis=1)
        self.bowling_df.loc[:, "Wickets Points"] = self.bowling_df.apply(lambda row: self.wicket(row["W"]), axis=1)
        self.bowling_df.loc[:, "No Ball Points"] = self.bowling_df.apply(lambda row: self.no_ball(row["NB"]), axis=1)
        self.bowling_df.loc[:, "Wide Ball Points"] = self.bowling_df.apply(
            lambda row: self.wide_ball(row["WD"]), axis=1
        )

        self.bowling_df.loc[:, "Bonus Bowling"] = self.bowling_df.apply(
            lambda row: self.bonus_bowling(row["W"]), axis=1
        )
        self.bowling_df.loc[:, "Economy Bowling"] = self.bowling_df.apply(
            lambda row: self.economy_bowling(row["ECON"]), axis=1
        )

        self.bowling_df.loc[:, "Total Bowling"] = (
            self.bowling_df["Maiden Points"]
            + self.bowling_df["Dot Ball Points"]
            + self.bowling_df["Wickets Points"]
            + self.bowling_df["No Ball Points"]
            + self.bowling_df["Wide Ball Points"]
            + self.bowling_df["Bonus Bowling"]
            + self.bowling_df["Economy Bowling"]
        )
        # Drop following columns
        # M, 0s, W, NB, WD, ECON
        # self.bowling_df.drop(columns=["M", "0s", "W", "NB", "WD", "ECON", "4s", "6s"], inplace=True)
        logging.info("Bowling score calculation completed")
        return self.bowling_df


# if __name__ == "__main__":
#     url = (
#         "https://www.espncricinfo.com/series/icc-cricket-world-cup-2023-24-1367856/afghanistan-vs-south-africa-42nd"
#         "-match-1384433/full-scorecard"
#     )
#     dfs = read_webpage(url)
#     first_batting = Batting(dfs[0])
#     first_batting.batting_preprocessing()
#     print(first_batting.batting_score_calculation())
#     first_bowling = Bowling(dfs[1])
#     first_bowling.bowling_preprocessing()
#     print(first_bowling.bowling_score_calculation())
#     second_batting = Batting(dfs[2])
#     second_batting.batting_preprocessing()
#     print(second_batting.batting_score_calculation())
#     second_bowling = Bowling(dfs[3])
#     second_bowling.bowling_preprocessing()
#     print(second_bowling.bowling_score_calculation())
