"""db model for sunsets/user account"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#QUESTION:
#how is the best way to organize the information in the db.Columns?
#also with the return .format in __repr__ functions

class User(db.Model):
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

    #QUESTION:
    #do i want to order by user_id?
    photos = db.relationship('Photo',
                              backref=db.backref('user'))

    favorites = db.relationship('UserFavorite',
                              backref=db.backref('user'))


    def __repr__(self):
        """Shows this information when user object is printed"""

        return '<User id={} name={} email={}'.format(
                                              self.user_id,
                                              self.user_name,
                                              self.user_email)

class Airport(db.Model):
    """Airports and their information"""

    __tablename__ = 'airports'

    #QUESTION:
    #would it make more sense to use icao code as airport ID?

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


    #QUESTION:
    #can this be named photo if the photo in Users is also named photo?
    photos = db.relationship('Photo',
                              backref=db.backref('airport'))


    def __repr__(self):
        """Shows this information when airport object is printed"""

        return '<Airport id={} code={} city={}'.format(
                                                self.airport_id,
                                                self.icao_code,
                                                self.city)


class UserFavorite(db.Model):
    """User's favorite airports"""

    __tablename__ = 'user_favorites'

    favorite_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.user_id'))
    airport_id = db.Column(db.Integer,
                            db.ForeignKey('airports.airport_id'))

    #I couldn't find a reason to use a backref here because why would you want
    #to reference who favorited the airport.
    #Actually, I guess thats something you could want.
    #I'll leave this note in incase I decide to do that in the future.

    airports = db.relationship('Airport')


    def __repr__(self):
        """Prints information for the user favorite object"""

        return '<User id={} user id={} airport={}'.format(
                                                   self.favorite_id,
                                                   self.user_id,
                                                   self.airport_id)


class Photo(db.Model):
    """User's uploaded photo"""

    __tablename__ = 'photos'

    photo_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'))
    airport_id = db.Column(db.Integer,
                         db.ForeignKey('airports.airport_id'))
    datetime = db.Column(db.DateTime)

    #QUESTION:
    #how many characters should i alot for a file name?
    filename = db.Column(db.String(100))

    #ratings subject to change depending on 2.0/3.0
    accuracy_rating = db.Column(db.Integer)
    sunset_rating = db.Column(db.Integer)

    description = db.Column(db.String(150))


    user = db.relationship('User',
                              backref=db.backref('photos'))


    def __repr__(self):
        """shows this when the photo object is printed"""

        return '<Photo id={} user={} date={} airport={}'.format(
                                                         self.photo_id,
                                                         self.user_id,
                                                         self.datetime,
                                                         self.airport_id)


def connect_to_db(app, db_uri='postgresql:///sunsets'):
    """Connects databse to Flask app"""

    #sunsets is the name of the db when doing createdb
    #set sunsets to default so that we can have the option
    #of using a test database :)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    #prints SQL translation:
    app.config['SQLALCHEMY_ECHO'] = True
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



