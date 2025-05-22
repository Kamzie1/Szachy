from . import db
from flask_login import UserMixin
from datetime import datetime
from enum import Enum
import sqlalchemy

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    date = db.Column(db.DateTime(), default = datetime.utcnow)

    elo = db.Column(db.Integer, default=1000)

    games_as_white = db.relationship('Game', back_populates='white_player',
                                     foreign_keys='Game.white_id', lazy='dynamic')
    games_as_black = db.relationship('Game', back_populates='black_player',
                                     foreign_keys='Game.black_id', lazy='dynamic')

    chat_user1 = db.relationship('Chat', back_populates='user1',
                                     foreign_keys='Chat.user1_id', lazy='dynamic')
    chat_user2 = db.relationship('Chat', back_populates='user2',
                                     foreign_keys='Chat.user2_id', lazy='dynamic')
    
    chat_user = db.relationship('Chat_log', back_populates='user',
                                     foreign_keys='Chat_log.nadawca', lazy='dynamic')

class ResultEnum(Enum):
    WHITE_WIN = 1
    DRAW = 0
    BLACK_WIN = -1

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer(), primary_key=True)
    result = db.Column(sqlalchemy.Enum(ResultEnum))
    date = db.Column(db.DateTime(), default = datetime.utcnow)

    white_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    black_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    white_elo = db.Column(db.Integer)
    black_elo = db.Column(db.Integer)

    white_player = db.relationship('User', foreign_keys=[white_id], back_populates='games_as_white')
    black_player = db.relationship('User', foreign_keys=[black_id], back_populates='games_as_black')


class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer(), primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='chat_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], back_populates='chat_user2')

    chat_log = db.relationship('Chat_log', back_populates='chat',
                                     foreign_keys='Chat_log.chat_id', lazy='dynamic')


class Chat_log(db.Model):
    __tablename__ = 'chat_logs'

    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), db.ForeignKey('chat.id'), nullable = False)
    nadawca = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    date = db.Column(db.DateTime(), default = datetime.utcnow)
    message = db.Column(db.String(1000))

    chat = db.relationship('Chat', foreign_keys=[chat_id], back_populates='chat_log')
    user = db.relationship('User', foreign_keys=[nadawca], back_populates='chat_user')