from sqlmodel import SQLModel, create_engine, Session
from src.common.models.article import Article
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

db_url = os.getenv("DATABASE_URI")

engine = create_engine(db_url, echo=True)


def connect():
    SQLModel.metadata.create_all(engine)


def update_articles(articles: list[Article]):
    with Session(engine) as session:
        try:
            for article in articles:
                session.add(article)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
