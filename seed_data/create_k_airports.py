"""Creates new file with only valid ICAO codes"""

import re


def write_to_new_file():
    """Takes only 4 letter codes from airports.csv and writes it to a new file"""

    #SOURCES: http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
    #ORIGINAL CSV FILE: http://ourairports.com/data/

    all_airports = open('airports.csv', 'r')

    icao_airports = open('icao_airports.csv', 'w')
    #Deleting the contents to prevent duplicate lines
    icao_airports.truncate()


    for line in all_airports:
        line = line.rstrip()
        information = line.split(',')
        code = information[1]

        # Using Regex to search for ICAO codes.
        #This means: 4 capital letters in a row
        match_obj = re.search(r'"[A-Z]{4}"', code)

        if match_obj:
            line_plus_new = "{}\n".format(line)
            icao_airports.write(line_plus_new)


    print "completed."


    icao_airports.close()
    all_airports.close()


write_to_new_file()









