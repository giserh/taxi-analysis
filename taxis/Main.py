import argparse
import Tkinter
import sys

import Results
import LoadData
import Metadata
import Graph
import WindowData

master = Tkinter.Tk() # Globally available instance of Tkinter

def terminate():
    """Finishing the performance"""
    master.destroy()
    print '\nGoodbye'
    sys.exit()


def print_help():
    """ Prints out the list of commands that can be used as an input """
    print 'List of available commands:'
    Results.print_help()
    Graph.print_help()
    print '  - load'
    print '  - subset_startend <ISO 8601 Time> <ISO 8601 Time>'
    print '  - subset_ids <id> <id> <id> ...'
    print '  - dataset <dataset>'
    print '  - file <starting_file>'
    print '  - meta <crawdad_xml_file>'
    print '  - help'
    print '  - quit'


def loop(dataset, id_file, id_list, results, window_data):
    """ Main loop og the program. Takes an input from the user and produces the result. """
    n = raw_input('Enter command: ').split(' ', 1)
    if n[0] == 'statistic':
        try:
            Results.process_result_request(n[1], results)
        except IndexError:
            print 'Enter a statistic to request. (\'help\' for more details)'
    elif n[0] == 'generate':
        try:
            Graph.process_graph_request(n[1], results, window_data)
        except IndexError:
            print 'Enter a graph to request. (\'help\' for more details)'
    elif n[0] == 'load':
        id_list = LoadData.load_ids(dataset + '/' + id_file)
        results = LoadData.calculate_results(id_list, dataset, LoadData.calculate_times(id_list, dataset))
    elif n[0] == 'subset_startend':
        results = LoadData.calculate_results(id_list, dataset, LoadData.parse_subset(n[1]))
    elif n[0] == 'subset_ids':
        id_list = LoadData.parse_ids(n[1])
        results = LoadData.calculate_results(id_list, dataset, LoadData.calculate_times(id_list, dataset))
    elif n[0] == 'dataset':
        try:
            dataset = 'datasets/' + n[1]
            id_list = LoadData.load_ids(dataset + '/' + id_file)
        except IndexError:
            print 'Enter a new dataset. (\'help\' for more details)'
    elif n[0] == 'file':
        try:
            id_file = n[1]
            id_list = LoadData.load_ids(dataset + '/' + id_file)
        except IndexError:
            print 'Enter a new starting file. (\'help\' for more details)'
    elif n[0] == 'meta':
        try:
            Metadata.process_meta(n[1])
        except IndexError, IOError:
            print 'Enter a crawdad_xml_file. (\'help\' for more details)'
    elif n[0] == 'help':
        print_help()
    elif n[0] == 'quit':
        terminate()
    else:
        print 'Invalid command.'
    master.after(2000, loop(dataset, id_file, id_list, results, window_data))

if __name__ == "__main__":
    master.protocol('WM_DELETE_WINDOW', terminate)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', help='The dataset to be analysed', required=False, default='cabspottingdata')
    parser.add_argument('-f', '--file', help='The starting file e.g. _cabs.txt', required=False, default='_cabs.txt')
    args = vars(parser.parse_args())

    print_help()

    dataset = 'datasets/' + args['dataset']
    id_file = args['file']
    id_list = LoadData.load_ids(dataset + '/' + id_file)
    results = None

    window_data = WindowData.WindowData(master)
    window_data.initialize()
    window_data.draw_background()

    master.after(2000, loop(dataset, id_file, id_list, results, window_data))
    master.mainloop()    
