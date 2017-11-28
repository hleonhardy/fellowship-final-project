from model import User
from model import connect_to_db, db
from server import app
from seed import load_airports


def load_fake_users():
    """ Loads test users """

    User.query.delete()

    user1 = User(user_name='SpongeBob',
                    user_email='sbob78@gmail.com',
                    user_pass= 'password')
    user2 = User(user_name='Squidward',
                    user_email='squid11@hotmail.com',
                    user_pass='squidlife')


    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()


def load_test_data():
    """ Loads user and airport data """

    load_fake_users()
    load_airports()




# **************************************************************************** #

if __name__ == '__main__':

    connect_to_db(app, 'postgresql:///testdb')
    db.drop_all()
    db.create_all()

    load_test_data()

