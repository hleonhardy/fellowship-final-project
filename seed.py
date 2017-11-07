"""Puts Airport data from icao_airports.csv into the airports table"""

from model import Airport, User, Photo, UserFavorite
from model import connect_to_db, db
from server import app

def load_airports():
    """load airport information into the airports table"""

    #Delete to prevent duplicates:
    Airport.query.delete()

    #opening the file created with only acceptable ICAO codes:
    with open('seed_data/icao_airports.csv') as airports_file:

        for line in airports_file:
            line = line.strip()
            information = line.split(',')

            #the [1:-1] is to get rid of quotation marks
            icao = information[1][1:-1]
            name = information[3][1:-1]

            lat = information[4]
            lon = information[5]

            country = information[8][1:-1]


            #information[9] gives 'US-CA' format.
            # state = information[9][3:]
            # city = information[10]

            #Apparently some lines in this file have something strange in
            #place of lattitude and longitude.
            #This just checks that lat and lon can be floats
            #If they aren't, we just don't add that line to the db.
            try:
                lat = float(lat)
                lon = float(lon)
            except:
                continue

            #instantiate airport object with given information
            #commenting out city and state for now because they aren't always
            #exactly city and state depending on the country
            airport = Airport(icao_code=icao,
                              lattitude=lat,
                              longitude=lon,
                              airport_name=name,
                              # city=city,
                              # state=state,
                              country=country)

            db.session.add(airport)

    db.session.commit()


if __name__ == '__main__':

  #db.create_all() inside connect_to_db()
  connect_to_db(app)

  load_airports()
