# THIS HAPPENS AFTER FORECAST HAS BEEN DETERMINED
#recall in server.py: forecast_json = find_forecast(code, sunset_datetime_obj)

from ratings_classes import (Rating,
                             BadRating,
                             LowCloudRating,
                             ClearSkyRating,
                             OnlyHighCloudRating,
                             MidFewRating,
                             MidSctRating)
from cloud_class import Cloud


################################################################################


def make_cloud_dict(forecast_json):
    """Given the correct forecast, returns categorized cloud dictionary"""

    #This is a list of cloud dictionaries
    lst_of_cloud_dicts = forecast_json['clouds']

    clouds = {'low': [0, 'SKC'], 'mid': [0, 'SKC'], 'high': [0, 'SKC']}

    #From the forecast data:
    for cloud_dict in lst_of_cloud_dicts:

        #Getting the right values
        cloud_code = cloud_dict['code']
        alt = cloud_dict['base_feet_agl']

        #instantiate cloud object:
        one_cloud = Cloud(cloud_code, alt)

        #We want the most cloud coverage per altitude range
        if one_cloud.amount > clouds[one_cloud.alt_type][0]:
            clouds[one_cloud.alt_type][0] = one_cloud.amount
            clouds[one_cloud.alt_type][1] = one_cloud.cloud_code

    #now we don't need the amounts anymore:
    for key in clouds:
        clouds[key] = clouds[key][1]


    return clouds


################################################################################


def return_rating(cat_cloud_dict):
    """Takes in cloud dict and returns a new dict with a rating and description"""

    #Broken or Overcast (These get the worst ratings)
    if 'BKN' in cat_cloud_dict.values() or 'OVC' in cat_cloud_dict.values():
        rating_obj = BadRating()
        # print "bad rating"

    #Low clouds present (no bkn or ovc)
    elif cat_cloud_dict['low'] != 'SKC':
        rating_obj = LowCloudRating()
        # print "low cloud rating"

    #Only clear skies/neutral rating
    elif cat_cloud_dict['low'] == 'SKC' and cat_cloud_dict['mid'] == 'SKC' and cat_cloud_dict['high'] == 'SKC':
        rating_obj = ClearSkyRating()
        # print "clear sky"

    #If there is nothing in mid (only high):
    elif cat_cloud_dict['mid'] == 'SKC':
        rating_obj = OnlyHighCloudRating()
        # print "high cloud, no bkn or ovc"

    #If mid clouds are few:
    elif cat_cloud_dict['mid'] == 'FEW':
        rating_obj = MidFewRating()
        # print "mid few"

    #If mid clouds are scattered (best rating):
    else:
        rating_obj = MidSctRating()
        # print "mid scattered"


    rating_num = rating_obj.get_number(cat_cloud_dict)


    return {'value': rating_num, 'description': rating_obj.description}



