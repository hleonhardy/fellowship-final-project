
class NoForecastDataError(Exception):
    """Error class for airports with no weather reports"""

    pass

class NoTimeZoneAvailable(Exception):
    """Error class for timezone library"""

    pass
