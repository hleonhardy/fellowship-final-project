from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.model):
    """A user class"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_name = db.Column(db.String(30),
                        nullable=False)
    user_email = db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    user_pass = db.Column(db.String(30),
                        nullable=False)

    #PUT RELATIONSHIPS HERE

    def __repr__(self):
        """Shows this information when object is printed"""

        return '<User id={} name={} email={}'.format(
                                              self.user_id,
                                              self.user_name,
                                              self.user_email)

class Airport(db.model):
    """Airports and their information"""

    __tablename__ = 'airports'

    airport_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    icao_code = db.Column(db.String(10),
                           nullable=False,
                           unique=True)
    lattitude = db.Column(db.Integer,
                           nullable=False)
    longitude = db.Column(db.Integer,
                           nullable=False)
    airport_name = db.Column(db.String(50))
    city = db.Column(db.String(30))
    state = db.Column(db.String(20))

    #PUT RELATIONSHIPS HERE

    def __repr__(self):
        """Shows this information when object is printed"""

        return '<Airport id={} code={} city={}'.format(
                                                self.airport_id,
                                                self.icao_code,
                                                self.city)




class UserFavorite(db.model):
    """User's favorite airports"""

    __tablename__ = 'user_favorites'

    favorite_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'))
    airport_id = db.Column(db.Integer,
                            db.ForeignKey('airports.airport_id'))


    #PUT RELATIONSHIPS HERE


    def __repr__(self):
        return '<User id={} user id={} airport={}'.format(
                                                   self.favorite_id,
                                                   self.user_id,
                                                   self.airport_id)



class Photo(db.model):
    """User's uploaded photo"""




def connect_to_db(app):
    """"""

    pass

