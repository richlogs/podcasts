import os
import sqlite3

import pandas as pd

from podcasts.init.loging import get_logger

logger = get_logger()


def set_dir():
    logger.info(f"Setting working directory")
    path = os.path.expanduser(
        "~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts"
    )
    os.chdir(path)
    logger.info(f"Set working directory to: {os.getcwd()}")


def db_connect(database: str = "Documents/MTLibrary.sqlite"):
    logger.info(f"Connecting to database: {database}")
    conn = sqlite3.connect(database)
    logger.info(f"Connected to database: {database}")
    return conn


def db_disconnect(conn):
    logger.info(f"Disconnecting from database")
    conn.close()
    logger.info(f"Disconnected from database")


query = """
SELECT
	datetime (ep.ZLASTDATEPLAYED + 978307200,
                "unixepoch",
                "utc") AS last_played,
	pod.ZTITLE AS podcast_title,
	ep.ZTITLE AS episode_title,
	coalesce(ep.ZWEBPAGEURL,pod.ZWEBPAGEURL) AS webpage_url,
	pod.ZFEEDURL,
	ep.ZENCLOSUREURL
FROM ZMTEPISODE AS ep
JOIN ZMTPODCAST AS pod ON pod.Z_PK = ep.ZPODCAST
ORDER BY ep.ZLASTDATEPLAYED ASC
"""


# Assuming you're using SQLite - change accordingly if using another database


if __name__ == "__main__":
    set_dir()
    # conn = db_connect()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM ZMTPODCAST")
    # podcasts = cursor.fetchall()
    # cursor.execute("SELECT * FROM ZMTEPISODE")
    # print(cursor.fetchall())
    # conn.close()

    conn = db_connect()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT * FROM ZMTEPISODE")

    # Fetch the results
    rows = cursor.fetchall()

    # Get column names and combine with table name
    columns = [f"{column[0]}" for column in cursor.description]

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Display the DataFrame
    print(df)
