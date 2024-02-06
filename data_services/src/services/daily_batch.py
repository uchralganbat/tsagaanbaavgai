from dotenv import load_dotenv, find_dotenv
import os
import logging
from src.common import db
import click
import logging
import os
from pathlib import Path


def main():

    session = db.connect(os.getenv("DATABASE_URI"))
    logging.info("Connected to database")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
