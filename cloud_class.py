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
        elif cloud_code == 'BKN':
            self.amount = 3
        else: #cloud_code = 'OVC':
            self.amount = 4

        self.cloud_code = cloud_code

        #cloud_base_ft_agl

        if alt < 6500 and alt > 0:
            self.alt_type = 'low'
        elif alt < 23000:
            self.alt_type = 'mid'
        elif alt >= 23000:
            self.alt_type = 'high'

        #This probably doesn't need to be here
        else:
            self.alt_type = 'none'

        self.alt = alt



