from math import sin, cos, asin, sqrt
import datetime

ONE_HOUR = datetime.timedelta(hours=1)

def num_hours(first, last):
    """
    Counts the number of horus between "first" and "last"
    """
    delta = last - first
    hours = (delta.days*24) + (delta.seconds/(60*60))
    return hours

def between(thing, start, end):
    """
    Works out if a thing is between the specified start and end points
    """
    if start < thing < end:
        return True
    return False

def haversine(previous_latitude, previous_longitude, latitude, longitude):
    """ Requires latitudes in radians """
    latitude_difference = latitude - previous_latitude
    longitude_difference = longitude - previous_longitude
    a = sin(latitude_difference/2)**2 + cos(previous_latitude) * cos(latitude) * sin(longitude_difference/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km