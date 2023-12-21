import numpy as np
import pandas as pd


def select_data(
    df: pd.DataFrame,
    columns: list[str] = ["title", "author", "duration", "download_date", "asset_url"],
) -> pd.DataFrame:
    return df[columns]


def convert_duration(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = pd.to_timedelta(df[col], unit="seconds").astype(str)
        df[col] = df[col].str.replace("0 days ", "")
        df[col] = df[col].apply(lambda x: x[:8])
        return df


def update_status(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        (df["playhead"] > 0) & (df["last_played"].notnull()),
        (df["playhead"] == 0) & (df["last_played"].notnull()),
        (df["last_played"].isnull()),
    ]

    values = ["listening", "finished", "unplayed"]

    # Creating the 'status' column based on the conditions and values
    df["status"] = np.select(conditions, values)

    return df


if __name__ == "__main__":
    from podcasts.utils.sqlite import get_podcast_data

    df = get_podcast_data()
    df = convert_duration(df, ["duration"])
    df = update_status(df)
