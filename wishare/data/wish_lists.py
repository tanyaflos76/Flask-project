import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Wish_list(SqlAlchemyBase):
    __tablename__ = 'wish_lists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    #   slug
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #   updated_at
    user = orm.relationship('User')
