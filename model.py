"""db model for sunsets/user account"""


from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.types import Geography


db = SQLAlchemy()


class User(db.Model):
    """A user class"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    user_pass = db.Column(db.String(30), nullable=False)

    #QUESTION:
    #do i want to order by user_id?


    def __repr__(self):
        """Shows this information when user object is printed"""

        return '<User id={} name={} email={}'.format(self.user_id,
                                                     self.user_name,
                                                     self.user_email)


class Airport(db.Model):
    """Airports and their information"""

    #******************** NOTE **********************#
    # In order to use geoalchemy2 you have to go into
    # sunsets db and type: 'CREATE EXTENSION postgis'
    # I did this with a source script in /scripts.
    #************************************************#

    __tablename__ = 'airports'

    #QUESTION:
    #would it make more sense to use icao code as airport ID?

    #commented out the city and state for now because they aren't neccesarily
    #city and state in countries besides US.

    airport_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    icao_code = db.Column(db.String(10), nullable=False, unique=True)
    lattitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    airport_name = db.Column(db.String(150))
    # city = db.Column(db.String(30))
    # state = db.Column(db.String(20))
    country = db.Column(db.String(20), nullable=True)

    #This is going to be the location
    #srid=4326 is default using negative values for lat/lon
    location = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)


    def __repr__(self):
        """Shows this information when airport object is printed"""

        return '<Airport id={} code={} name={}>'.format(self.airport_id,
                                                       self.icao_code,
                                                       self.airport_name)


class UserFavorite(db.Model):
    """User's favorite airports"""

    __tablename__ = 'user_favorites'

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    favorite_title = db.Column(db.String(25))

    favorite_lat = db.Column(db.Float)
    favorite_lng = db.Column(db.Float)
    favorite_location = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)

    #Foreign keys:
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.airport_id'))

    #I couldn't find a reason to use a backref here because why would you want
    #to reference who favorited the airport.
    #Actually, I guess thats something you could want.
    #I'll leave this note in incase I decide to do that in the future.

    #Relationships:
    user = db.relationship('User', backref=db.backref('favorites'))
    airports = db.relationship('Airport')

    def __repr__(self):
        """Prints information for the user favorite object"""

        return '<UserFavorite id={} user id={} airport={}>'.format(self.favorite_id,
                                                          self.user_id,
                                                          self.airport_id)


class Photo(db.Model):
    """User's uploaded photo"""

    __tablename__ = 'photos'

    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #Foreign keys:
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.airport_id'))

    photo_title = db.Column(db.String(25))

    photo_lat = db.Column(db.Float)
    photo_lng = db.Column(db.Float)
    photo_location = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    airport_dist = db.Column(db.Float)

    datetime = db.Column(db.DateTime)

    filepath = db.Column(db.String(100))

    sunset_rating = db.Column(db.Integer)

    description = db.Column(db.String(150))

    #Relationships:
    user = db.relationship('User', backref=db.backref('user_photos'))
    airport = db.relationship('Airport', backref=db.backref('airport_photos'))


    def __repr__(self):
        """shows this when the photo object is printed"""

        return '<Photo id={} user={} date={} airport={}'.format(self.photo_id,
                                                                self.user_id,
                                                                self.datetime,
                                                                self.airport_id)


class UserFavoritePhoto(db.Model):
    """Links a photo to a user's favorited location."""

    __tablename__ = 'user_favorite_photos'

    favorite_photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    photo_id = db.Column(db.Integer, db.ForeignKey('photos.photo_id'))
    favorite_id = db.Column(db.Integer, db.ForeignKey('user_favorites.favorite_id'))


    def __repr__(self):
        """shows this when the photo object is printed"""

        return '<Photo id={} favorite_id={}'.format(self.photo_id, self.favorite_id)



def connect_to_db(app, db_uri='postgresql:///sunsets'):
    """Connects databse to Flask app"""

    #sunsets is the name of the db when doing createdb
    #set sunsets to default so that we can have the option
    #of using a test database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    #prints SQL translation:
    app.config['SQLALCHEMY_ECHO'] = False
    #stops the yelling
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #flask app
    db.app = app
    db.init_app(app)

    db.create_all()


if __name__ == '__main__':

    from server import app
    connect_to_db(app)


    print "CONNECTED TO DB!"



