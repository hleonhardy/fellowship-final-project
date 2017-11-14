# THIS HAPPENS AFTER FORECAST HAS BEEN DETERMINED
#recall in server.py: forecast_json = find_forecast(code, sunset_datetime_obj)

from ratings_classes import (
                            Rating,
                            BadRating,
                            LowCloudRating,
                            ClearSkyRating,
                            OnlyHighCloudRating,
                            MidFewRating,
                            MidSctRating
                            )
from cloud_class import Cloud

################################################################################
#SAMPLE DATA:
cloud_dict_1 = {"clouds": [
                        {
                            "cloud_base_ft_agl": 0,
                            "cloud_base_meters_agl": 0,
                            "cloud_code": "SKC",
                            "cloud_text": "Clear skies"
                        }
                    ]
                }

cloud_dict_2 = {"clouds": [
                        {
                            "cloud_base_ft_agl": 7000,
                            "cloud_code": "BRK"
                        },
                        {
                            "cloud_base_ft_agl": 500,
                            "cloud_code": "SCT"
                        }
                    ]
                }


sample_dict_1 = {'high': 'SKC', 'low': 'SCT', 'mid': 'BRK'}
sample_dict_2 = {'high': 'SKC', 'low': 'SKC', 'mid': 'SKC'}
sample_dict_3 = {'high': 'SKC', 'low': 'SKC', 'mid': 'SCT'}
sample_dict_4 = {'high': 'SCT', 'low': 'SCT', 'mid':'SKC'}
sample_dict_5 = {'high': 'SCT', 'low': 'SKC', 'mid': 'SKC'}
sample_dict_6 = {'low': 'SKC', 'mid': 'FEW', 'high': 'FEW'}
sample_dict_7 = {'low': 'SKC', 'mid': 'SCT', 'high': 'FEW'}

################################################################################

def make_cloud_dict(forecast_json):
    """Given the correct forecast, returns categorized cloud dictionary"""

    #This is a list of cloud dictionaries
    lst_of_cloud_dicts = forecast_json['clouds']

    clouds = {'low': [0, 'SKC'], 'mid': [0, 'SKC'], 'high': [0, 'SKC']}

    #From the forecast data:
    for cloud_dict in lst_of_cloud_dicts:

        #Getting the right values
        cloud_code = cloud_dict['cloud_code']
        alt = cloud_dict['cloud_base_ft_agl']

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



def return_rating(cat_cloud_dict):
    """Takes in cloud dict and returns a new dict with a rating and description"""

    #Broken or Overcast (These get the worst ratings)
    if  'BRK' in cat_cloud_dict.values() or 'OVO' in cat_cloud_dict.values():
        rating_obj = BadRating()

    #Low clouds present (no brk or ovo)
    elif  cat_cloud_dict['low'] != 'SKC':
        rating_obj = LowCloudRating()

    #Only clear skies/neutral rating
    elif cat_cloud_dict['low'] == 'SKC' and cat_cloud_dict['mid'] == 'SKC' and cat_cloud_dict['high'] == 'SKC':
        rating_obj = ClearSkyRating()

    #If there is nothing in mid (only high):
    elif cat_cloud_dict['mid'] == 'SKC':
        rating_obj = OnlyHighCloudRating()

    #If mid clouds are few:
    elif cat_cloud_dict['mid'] == 'FEW':
        rating_obj = MidFewRating()

    #If mid clouds are scattered (best rating):
    else:
        rating_obj = MidSctRating()


    rating_num = rating_obj.get_number(cat_cloud_dict)
    return [rating_num, rating_obj.description]




print return_rating(sample_dict_7)



