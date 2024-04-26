import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String, nullable=False)
