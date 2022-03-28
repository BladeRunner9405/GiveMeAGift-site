import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Pictures(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, nullable=False)
    present_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("wishes.id"), nullable=False)
    picture = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relation('Wishes')
