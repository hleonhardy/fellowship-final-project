# THIS HAPPENS AFTER FORECAST HAS BEEN DETERMINED
#recall in server.py: forecast_json = find_forecast(code, sunset_datetime_obj)



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


################################### CLASSES ####################################
    #RECALL:
    #LOW: 0 --> 6500
    #MED: 6500 --> 23000
    #HIGH: 23000 --> infinity

class Cloud(object):
    """A cloud object"""

    def __init__(self, cloud_code, alt):

        #"cloud_code"

        #So that we can have only the most clouds per alt type

        if cloud_code == 'SKC':
            self.amount = 0
        elif cloud_code == 'FEW':
            self.amount = 1
        elif cloud_code == 'SCT':
            self.amount = 2
        elif cloud_code == 'BRK':
            self.amount = 3
        else: #cloud_code = 'OVO':
            self.amount = 4

        self.cloud_code = cloud_code

        #cloud_base_ft_agl

        if alt < 6500 and alt > 0:
            self.alt_type = 'low'
        elif alt < 23000:
            self.alt_type = 'mid'
        elif alt >= 23000:
            self.alt_type = 'high'
        else:
            self.alt_type = 'none'


        self.alt = alt


class Rating(object):
    """A rating object"""


    def get_number(self, cat_cloud_dict):

        #What will be in the hundreds, tens, and ones place of our rating #
        hun_ten_one = [None, None, None]

        for key in cat_cloud_dict:
            if cat_cloud_dict[key] == 'SKC':
                self.rating = self.skc
            elif cat_cloud_dict[key] == 'FEW':
                self.rating = self.few
            elif cat_cloud_dict[key] == 'SCT':
                self.rating = self.sct
            elif cat_cloud_dict[key] == 'BRK':
                self.rating = self.brk
            else: #cat_cloud_dict[key] == 'OVO':
                self.rating = self.ovo

            if key == self.hundreds:
                hun_ten_one[0] = self.rating

            elif key == self. tens:
                hun_ten_one[1] = self.rating

            else: #key == self.ones:
                hun_ten_one[2] = self.rating

        rating_num = "{}{}{}".format(hun_ten_one[0], hun_ten_one[1], hun_ten_one[2])

        return rating_num



class BadRating(Rating):
    """BRK/OVO or low cloud object"""


    def __init__(self):

        self.skc = 0
        self.few = 1
        self.sct = 2
        self.brk = 3
        self.ovo = 4

        self.hundreds = 'low'
        self.tens = 'mid'
        self.ones = 'high'

        self.description = "Sunset is too cloudy!"

    def get_number(self, cat_cloud_dict):

        rating_num = super(BadRating, self).get_number(cat_cloud_dict)
        #This is a bad rating so make the number negative and even more negatvie
        #by adding an extra zero.
        bad_rating_num = int("-{}0".format(rating_num))

        return bad_rating_num



class LowCloudRating(Rating):
    """Rating for just low clouds, no BRK or OVO"""

    def __init__(self):

        self.skc = 0
        self.few = 1
        self.sct = 2
        self.brk = 3
        self.ovo = 4

        self.hundreds = 'low'
        self.tens = 'mid'
        self.ones = 'high'

        self.description = "Clouds too low for perfect sunset!"

    def get_number(self, cat_cloud_dict):

        rating_num = super(LowCloudRating, self).get_number(cat_cloud_dict)
        #This is a bad rating so make the number negative
        low_cloud_rating_num = int("-{}".format(rating_num))

        return low_cloud_rating_num


class ClearSkyRating(object):
    """Rating object for clear skies"""

    def __init__(self):

        self.description = "Totally clear skies for sunset!"


    def get_number(self, cat_cloud_dict):
        """Returns 0 because clear sky is neutral rating"""
        #Takes in cat_cloud_dict for consistancy when called
        #we obiously don't need to use it here

        return 0


class OnlyHighCloudRating(Rating):
    """Rating object for only high level clouds"""

    def __init__(self):

        self.skc = 0
        self.few = 1
        self.sct = 2

        self.hundreds = 'mid'
        self.tens = 'high'
        self.ones = 'low'

        self.description = "Sunset is decent-lower clouds would be preferable though."


    def get_number(self, cat_cloud_dict):

        #Nothing we need to change with this one.
        rating_num = super(OnlyHighCloudRating, self).get_number(cat_cloud_dict)
        rating_num = int(rating_num)

        return rating_num


class MidFewRating(Rating):
    """Rating object for good skies with mid level few clouds"""

    def __init__(self):

        self.skc = 2
        self.few = 1
        self.sct = 0

        self.hundreds = 'mid'
        self.tens = 'high'
        self.ones = 'low'

        self.description = "Great sunset! Just a few more mid level clouds and it would be perfect."


    def get_number(self, cat_cloud_dict):

        #Nothing we need to change with this one.
        rating_num = super(MidFewRating, self).get_number(cat_cloud_dict)
        #since few is 1 in this case we will just need to make the scattered a
        #higher number so that fewer is not as good as scattered
        rating_num = int(rating_num)

        return rating_num 


class MidSctRating(Rating):
    """Rating object for good skies with mid level few clouds"""

    def __init__(self):

        self.skc = 2
        self.few = 1
        self.sct = 0

        self.hundreds = 'mid'
        self.tens = 'high'
        self.ones = 'low'

        self.description = "Perfect Sunset!"


    def get_number(self, cat_cloud_dict):

        #Nothing we need to change with this one.
        rating_num = super(MidSctRating, self).get_number(cat_cloud_dict)
        #Since sct is a 0, we should put a 2 in the front so that
        #scattered is a higher number and therefore 'better'
        rating_num = int('2{}'.format(rating_num[1:]))
        

        return rating_num 



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

        if one_cloud.amount > clouds[one_cloud.alt_type][0]:
            clouds[one_cloud.alt_type][0] = one_cloud.amount
            clouds[one_cloud.alt_type][1] = one_cloud.cloud_code

    #now we don't need the amounts anymore:

    for key in clouds:
        clouds[key] = clouds[key][1]

    return clouds



def return_rating_dict(cat_cloud_dict):
    """Takes in cloud dict and returns a new dict with a rating and description"""

    #Broken or Overcast (These get the worst ratings)
    if  'BRK' in cat_cloud_dict.values() or 'OVO' in cat_cloud_dict.values():
        rating_obj = BadRating()

    #Low clouds present
    elif  cat_cloud_dict['low'] != 'SKC':
        rating_obj = LowCloudRating()

    #Only clear skies
    elif cat_cloud_dict['low'] == 'SKC' and cat_cloud_dict['mid'] == 'SKC' and cat_cloud_dict['high'] == 'SKC':
        rating_obj = ClearSkyRating()

    #If there is nothing in mid:
    elif cat_cloud_dict['mid'] == 'SKC':
        rating_obj = OnlyHighCloudRating()

    #If mid clouds are few:
    elif cat_cloud_dict['mid'] == 'FEW':
        rating_obj = MidFewRating()

    #If mid clouds are scattered:
    else:
        rating_obj = MidSctRating()


    rating_num = rating_obj.get_number(cat_cloud_dict)
    print [rating_num, rating_obj.description]


return_rating_dict(sample_dict_7)













