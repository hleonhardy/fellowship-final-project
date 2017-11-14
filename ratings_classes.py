"""Classes for each rating category"""


class Rating(object):
    """A rating object"""


    def get_number(self, cat_cloud_dict):
        """Returns a base rating value that can be modified for rating sublcasses"""

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

            #Places change for subclasses so we are making sure whatever
            #value we have for each place is in the right place.
            if key == self.hundreds:
                hun_ten_one[0] = self.rating

            elif key == self. tens:
                hun_ten_one[1] = self.rating

            else: #key == self.ones:
                hun_ten_one[2] = self.rating

        rating_num = "{}{}{}".format(hun_ten_one[0], hun_ten_one[1], hun_ten_one[2])


        return rating_num



class BadRating(Rating):
    """BRK/OVO cloud object"""

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
