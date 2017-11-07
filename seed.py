"""Puts Airport data from icao_airports.csv into the airports table"""

from model import Airport, User, Photo, UserFavorite
from model import connect_to_db, db
from server import app

def load_airports():
    """load airport information into the airports table"""

    #Delete to prevent duplicates:
    Airport.query.delete()

    with open('seed_data/icao_airports.csv') as airports_file:

        for line in airports_file:
            line = line.strip()
            information = line.split(',')

            icao = information[1]
            name = information[3]

            lat = information[4]
            lon = information[5]

            lat = float(lat)
            lon = float(lon)

            print lat, type(lat)
            print lon, type(lon)

            country = information[8]
            state = information[9][3:]
            city = information[10]

            print country

            #instantiate airport object with given information
            airport = Airport(icao_code=icao,
                              lattitude=lat,
                              longitude=lon,
                              airport_name=name,
                              city=city,
                              state=state)
                              # country=country)

            db.session.add(airport)
            break


    db.session.commit()


if __name__ == '__main__':
  
  connect_to_db(app)
  db.create_all()  

  load_airports()



