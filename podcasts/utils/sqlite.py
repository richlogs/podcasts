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

    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e

    return df


if __name__ == "__main__":
    set_dir()

    query = """
        SELECT *
        FROM ZMTEPISODE
        WHERE ZASSETURL IS NOT NLL
    """

    df = query_database(query)
    print(df)
