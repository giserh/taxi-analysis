class LocationNotFoundException(Exception):
    """
    Exception to handle locations not found for graphing
    """
    pass


class Graph:
    """
    Responsible for drawing graphs of popular locations
    """
    def __init__(self, locations, paths, window_data):
        """
        Initialises a new graph window
        """
        self.nodes = []
        for location in locations:
            if ((location[1] < window_data.min_long) or
                    (location[0] > window_data.min_lat) or
                    (location[1] > window_data.max_long) or
                    (location[0] < window_data.max_lat)):
                continue
            else:
                self.nodes.append(location)

        self.nodes.sort()
        self.links = []
        for i in xrange(len(self.nodes)):
            self.links.append([])
        for path in paths:
            for index in xrange(len(path)-1):
                if path[index][2] == 1: # Only track drives where the cab had a passenger in it
                    try:
                        loc1_index = self.get_index(path[index])
                        loc2_index = self.get_index(path[index + 1])
                        self.links[loc1_index].append(loc2_index)
                    except LocationNotFoundException:
                        continue

    def get_index(self, node):
        """
        Searches for the index of a particular location node
        """
        imin = 0
        imax = len(self.nodes) - 1

        while imax >= imin:
            imid = (imin + imax) / 2

            
            if self.nodes[imid] == node:
                return imid
            elif self.nodes[imid] < node:
                imin = imid + 1
            else:
                imax = imid - 1
        raise LocationNotFoundException

    def draw_locations(self, window_data):
        """
        Draws the locations on the window
        """
        for index in xrange(len(self.nodes)):
            window_data.draw_circle(self.nodes[index][0], self.nodes[index][1], 'blue', 2)

    def draw_degree_centrality(self, window_data):
        """
        Plots the degrees of centrality on the graphy
        """
        max_links = 0
        for index in xrange(len(self.nodes)):
            max_links = max(len(self.links[index]), max_links)
        for index in xrange(len(self.nodes)):
            color_value = float(len(self.links[index]))/max_links
            color = interpolate_color(color_value)
            window_data.draw_circle(self.nodes[index][0], self.nodes[index][1], color, 2)

def interpolate_color(x):
    """
    Returns correct colour for graph based on popularity
    """
    if x == 0:
        return 'medium slate blue'
    elif x < 0.05:
        return 'deep sky blue'
    elif x < 0.1:
        return 'yellow'
    elif x < 0.15:
        return 'orange'
    elif x < 0.2:
        return 'dark orange'
    else:
        return 'red'

def process_graph_request(request, results, window_data):
    """
    Starts the graphing process
    """
    if results is None:
        print 'No dataset has been loaded.'
        return
    graph = Graph(results.locations, results.paths, window_data) 
    if request == 'locations':
        graph.draw_locations(window_data)
    elif request == 'degree_centrality':
        graph.draw_degree_centrality(window_data)
    else:
        print 'Invalid graph requested.'

def print_help():
    """
    Returns help message for this module
    """
    print '  - generate locations'
    print '  - generate degree_centrality'