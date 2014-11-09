import datetime

class Results:
    """
    Represents the output result set from the input data set
    """
    def __init__(self):
        """
        Creates a new result set
        """
        self.num_uniques = 0  # num of unique ids in the whole dataset
        self.num_uniques_over_time = []  # numbers showing how many cabs were active at a certain time
        self.first_time = None
        self.ids = []
        self.distances = []
        self.speeds = []
        self.efficiencies = []
        self.locations = []
        self.paths = []


    def print_num_uniques(self):
        """
        Prints the number of unique cabs in one dataset
        """
        print 'There are', self.num_uniques, 'unique cabs in this dataset.'

    def print_num_uniques_over_time(self):
        """
        Prints the number of unique entries over a subset of data
        """
        if not self.num_uniques_over_time:
            print 'The dataset and the given subset do not intersect.'
        time = self.first_time
        one_hour = datetime.timedelta(hours=1)
        for i in self.num_uniques_over_time:
            print time.isoformat(), '->', i, 'unique cabs'
            time += one_hour

    def print_distances(self):
        """
        Prints the distances each cab travels
        """
        for this_id, distance in enumerate(self.distances):
            print self.ids[this_id] + ' travelled ' + str(distance) + ' km'

    def print_speeds(self):
        """
        Prints the average speed of each cab
        """
        for this_id, speed in enumerate(self.speeds):
            print self.ids[this_id] + ' had an average speed of ' + str(speed) + ' km/h'

    def print_efficiencies(self):
        """
        Prints, as a percentage, the time each each cab was being utilised (ie was being efficient)
        """
        for this_id, efficiency in enumerate(self.efficiencies):
            print self.ids[this_id] + ' was ' + str(efficiency) + '% efficient.'


    def create_chart(self, data, names, chartname):
        """
        Calls the chart class to generate charts of the data
        """
        charts = Charts.Charts()
        charts.draw_chart(data, names, chartname)

    def print_who_moved_most(self):
        """
        Prints the cab which moved the most
        """
        print self.ids[self.distances.index(max(self.distances))]

    def print_fastest_cab(self):
        """
        Prints the cab which moved fastest
        """
        print self.ids[self.speeds.index(max(self.speeds))]

    def print_slowest_cab(self):
        """
        Prints the cab which moved slowest
        """
        print self.ids[self.speeds.index(min(self.speeds))]


    def add_uniques_over_time(self, cab_over_time):
        """
        Adds a cab to the set of 'uniques' if applicable
        """
        self.num_uniques_over_time = [a + b for a, b in zip(self.num_uniques_over_time, cab_over_time)]
        if sum(cab_over_time) > 0:
            self.num_uniques += 1

    def merge_locations(self, new_locations):
        """
        Merges two 'locations' into one
        """
        for new_node in new_locations:
            self.locations.append(new_node)
        self.locations = list(set(self.locations))

    def add_record(self, this_id, records):
        """
        Adds a new cab record to the result set
        """
        self.ids.append(this_id)
        self.add_uniques_over_time(records.over_time)
        self.distances.append(records.distance)
        self.speeds.append(records.speed)
        self.efficiencies.append(records.efficiency)
        self.merge_locations(records.locations)
        self.paths.append(records.locations)

def process_result_request(statistic, results):
    """
    Processes the request for some statistic detail
    """
    if results is None:
        print 'No dataset has been loaded.'
        return
    if statistic == 'uniques':
        results.print_num_uniques()
    elif statistic == 'over_time':
        results.print_num_uniques_over_time()
    elif statistic == 'distances':
        results.print_distances()
    elif statistic == 'speeds':
        results.print_speeds()
    elif statistic == 'efficiencies':
        results.print_efficiencies()
    elif statistic == 'moved_most':
        results.print_who_moved_most()
    elif statistic == 'fastest_cab':
        results.print_fastest_cab()
    elif statistic == 'slowest_cab':
        results.print_slowest_cab()
    elif statistic == "e":
        results.print_efficiencies()
    else:
        print 'Invalid statistic requested.'

def print_help():
    """
    Returns help for the methods available
    """
    print '  - statistic uniques'
    print '  - statistic over_time'
    print '  - statistic distances'
    print '  - statistic speeds'
    print '  - statistic efficiencies'
    print '  - statistic moved_most'
    print '  - statistic fastest_cab'
    print '  - statistic slowest_cab'
