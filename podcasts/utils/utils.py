import os
import sqlite3

from podcasts.init.loging import get_logger

logger = get_logger()


def set_dir():
    logger.info(f"Setting working directory")
    os.chdir("~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts")
    logger.info(f"Set working directory to: {os.getcwd()}")


def db_connect(database: str = "Documents/MTLibrary.sqlite"):
    logger.info(f"Connecting to database: {database}")
    conn = sqlite3.connect(database)
    logger.info(f"Connected to database: {database}")
    return conn


if __name__ == "__main__":
    set_dir()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ZMTPODCAST")
    print(cursor.fetchall())
    conn.close()
