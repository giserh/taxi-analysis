import Tkinter


class WindowData:
    """
    A Tkinter window for displaying graphs
    """
    def __init__(self, master):
        self.master = master
        self.window = None
        self.window_title = 'San Francisco'
        self.img_file = './SF.gif'
        self.img = None
        # These 6 variables should correspond to the image in img_file.
        self.width = 1050
        self.height = 790
        self.min_lat = 37.813988
        self.max_lat = 37.706776
        self.min_long = -122.530003
        self.max_long = -122.349415

    def initialize(self):
        """
        Creates the Tkinter window
        """
        self.master.wm_title(self.window_title)
        self.window = Tkinter.Canvas(self.master, width=self.width, height=self.height)
        self.window.pack()

    def long_to_pixel(self, longitude):
        """
        Converts a longitude into a pixel for location
        """
        horizontal = (self.min_long - longitude)/(self.min_long - self.max_long)
        return horizontal * self.width

    def lat_to_pixel(self, latitude):
        """
        Converts a latitude into a pixel for location
        """
        vertical = (self.min_lat - latitude)/(self.min_lat - self.max_lat)
        return vertical * self.height

    def draw_background(self):
        """
        Draws the background image
        """
        self.img = Tkinter.PhotoImage(file=self.img_file)
        self.window.create_image(0, 0, image=self.img, anchor='nw')

    def draw_circle(self, latitude, longitude, color, size):
        """
        Draws a circle on the screen between two coordinates
        """
        horizontal = self.long_to_pixel(longitude)
        vertical = self.lat_to_pixel(latitude)
        self.window.create_oval(horizontal-size, vertical-size, horizontal+size, vertical+size, outline=color, fill=color, width=1)

    def draw_line(self, lat1, long1, lat2, long2, color, size):
        """
        Draws a line on the screen between two coordinates
        """
        horizontal1 = self.long_to_pixel(long1)
        vertical1 = self.lat_to_pixel(lat1)
        horizontal2 = self.long_to_pixel(long2)
        vertical2 = self.lat_to_pixel(lat2)
        self.window.create_line(horizontal1, vertical1, horizontal2, vertical2, fill=color, width=size)