from typing import Optional
from sqlmodel import Field, SQLModel


class Article(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    headline: str
    url: str
    author: str
    title: str
    category: str
    source: str
    date: str
    content: str
