import numpy as np
import pandas as pd

import podcasts.init.loging as logging

logger = logging.get_logger()


def select_data(
    df: pd.DataFrame,
    columns: list[str] = [
        "title",
        "author",
        "status",
        "duration",
        "download_date",
        "asset_url",
    ],
) -> pd.DataFrame:
    return df[columns]

def format_columns(df):
    df.columns = [' '.join(col.title().split('_')) for col in df.columns]
    return df

def convert_datetime(
    df: pd.DataFrame, columns: list, time_zone: str = "Pacific/Auckland"
) -> pd.DataFrame:
    # Converts timezone to nz time.
    # The inital tz_convert converts time to UTC, why? I don't know.
    # The second tz_convert converts time to the desired timezone.
    logger.info(f"Converting {columns=} to {time_zone} time.")
    for col in columns:
        df[col] = pd.to_datetime(df[col]).dt.tz_localize("UTC")
        df[col] = df[col].dt.tz_convert(time_zone)
        df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
        df[col] = pd.to_datetime(df[col]).dt.tz_localize("UTC")
        df[col] = df[col].dt.tz_convert(time_zone).dt.tz_localize(None)

    return df


def convert_duration(
    df: pd.DataFrame, columns: list[str] = ["duration"]
) -> pd.DataFrame:
    for col in columns:
        df[col] = pd.to_timedelta(df[col], unit="seconds").astype(str)
        df[col] = df[col].str.replace("0 days ", "")
        df[col] = df[col].apply(lambda x: x[:8])
        return df


def add_status(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        (df["playhead"] > 0) & (df["last_played"].notnull()),
        (df["playhead"] == 0) & (df["last_played"].notnull()),
        (df["last_played"].isnull()),
    ]

    values = ["Listening", "Played", "Unplayed"]

    # Creating the 'status' column based on the conditions and values
    df["status"] = np.select(conditions, values)

    return df


if __name__ == "__main__":
    from podcasts.utils.dbops import get_podcast_data

    df = get_podcast_data()
    df = convert_datetime(df, ["last_played", "download_date"])
    df = convert_duration(df, ["duration"])
    df = add_status(df)
    print(select_data(df))
