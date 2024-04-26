import sqlalchemy
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)