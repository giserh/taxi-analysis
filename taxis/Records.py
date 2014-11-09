import datetime
from math import radians
from Utility import *


class Records:
    """
    Parses/stores the record for one cab
    """
    def __init__(self):
        """ Initialises all the fields. """
        self.times = []
        self.passengers = []
        self.latitudes = []
        self.longitudes = []
        self.over_time = None # list of 0 and 1s (1 if a cab had a record at a certain time)
        self.distance = 0
        self.speed = None
        self.efficiency = 0
        self.locations = []
        self.times_moved = 0

    def calculate_statistics(self, lines, first, hours):
        """ Updates the fields from the uploaded data """
        for i in reversed(lines):
            self.times.append(extract_time(i))
            self.passengers.append(extract_passenger(i))
            self.latitudes.append(extract_latitude(i))
            self.longitudes.append(extract_longitude(i))
        self.calculate_over_time(first, hours)
        self.calculate_distance()
        self.calculate_speed()
        self.calculate_efficiency()
        self.calculate_locations()


    def calculate_over_time(self, first, hours):
        """ Calculates the change over the specified time range """
        self.over_time = [0] * hours
        index = 0
        current_time = first
        for time in self.times:
            while time > current_time:
                if between(time, current_time, current_time + ONE_HOUR) and not self.over_time[index]:
                    self.over_time[index] = 1
                index += 1
                current_time += ONE_HOUR
                if index == hours:
                    return

    def calculate_distance(self):
        """ Calculates the distance that was made since the last time by a cab. """
        previous_latitude = radians(self.latitudes[0])
        previous_longitude = radians(self.longitudes[0])
        for latitude, longitude in zip(map(radians, self.latitudes), map(radians, self.longitudes)):
            self.distance += haversine(previous_latitude, previous_longitude, latitude, longitude)
            previous_latitude = latitude
            previous_longitude = longitude

    def calculate_speed(self):
        """ Calculates the overall speed of the cab """
        total_time = self.get_total_time()
        self.speed = self.distance / (0.000277778 * total_time.total_seconds())

    def calculate_efficiency(self):
        """ Calculates the efficiency (in percents) of a cab over the whole time """
        efficient_time = datetime.timedelta()
        total_time = self.get_total_time()
        previous_time = self.times[0]
        previous_passenger = self.passengers[0]
        for time, passenger in zip(self.times, self.passengers):
            if previous_passenger:
                efficient_time += time - previous_time
            previous_time = time
            previous_passenger = passenger
        self.efficiency = (efficient_time.total_seconds() / total_time.total_seconds()) * 100

    def calculate_locations(self):
        """ Adds a new location to the list """
        rounding_num = 3
        previous_passenger = self.passengers[0]
        for passenger, latitude, longitude in zip(self.passengers, [round(l, rounding_num) for l in self.latitudes],
                                                  [round(l, rounding_num) for l in self.longitudes]):
            if passenger != previous_passenger:
                self.locations.append((latitude, longitude, passenger))
                previous_passenger = passenger

    def get_total_time(self):
        """ Returns the total time of work of the cab """
        return self.times[-1] - self.times[0]


def extract_time(line):
    """ Returns a timestamp from the text line """
    return datetime.datetime.fromtimestamp(int(line.split(' ')[3]))


def extract_passenger(line):
    """ Returns true if a cab had a passenger (from the text line) """
    return bool(int(line.split(' ')[2]))


def extract_latitude(line):
    """ Returns the latitude from the text line"""
    return float(line.split(' ')[0])


def extract_longitude(line):
    """ Returns the longitude from the text line """
    return float(line.split(' ')[1])
