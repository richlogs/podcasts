import os
import sqlite3

import pandas as pd

from podcasts.init.loging import get_logger

logger = get_logger()


def set_dir(
    directory: str = "~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts",
):
    path = os.path.expanduser(directory)
    os.chdir(path)
    logger.info(f"Working directory set to: {path}")


def query_database(
    query: str, database: str = "Documents/MTLibrary.sqlite"
) -> pd.DataFrame:
    try:
        database_path = os.path.join(os.getcwd(), database)
        logger.info(f"Connecting to database: {database_path}")
        with sqlite3.connect(database_path) as conn:
            df = pd.read_sql_query(query, conn)
        logger.info("Query executed successfully.")
        logger.info(
            f"Returned dataframe with {len(df)} rows and {len(df.columns)} columns"
        )

    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e

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
        df[col] = df[col].dt.tz_convert(time_zone)

    return df


def build_standard_query() -> str:
    columns = [
        "ZTITLE AS title",
        "ZAUTHOR AS author",
        "ZPODCAST AS podcast",
        "ZDURATION AS duration",
        "ZPLAYHEAD AS playhead",
        "ZITEMDESCRIPTIONWITHOUTHTML AS description",
        "ZASSETURL AS asset_url",
        "ZPODCASTUUID AS podcast_uuid",
        "ZUUID AS uuid",
    ]
    query = f"""
        SELECT {', '.join(columns)},
        datetime(ZLASTDATEPLAYED + 978307200, "unixepoch", "utc") AS last_played,
        datetime(ZDOWNLOADDATE + 978307200, "unixepoch", "utc") AS download_date
        FROM ZMTEPISODE
        WHERE ZASSETURL IS NOT NULL
        ORDER BY ZDOWNLOADDATE DESC
    """

    return query


def get_podcast_data() -> pd.DataFrame:
    set_dir()
    query = build_standard_query()
    df = query_database(query)
    df = convert_datetime(df, ["last_played", "download_date"])
    return df


if __name__ == "__main__":
    set_dir()

    query = build_standard_query()

    df_episodes = query_database(query)
    df_episodes = convert_datetime(df_episodes, ["last_played", "download_date"])

    print(df_episodes)
