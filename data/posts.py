import sqlalchemy
from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
