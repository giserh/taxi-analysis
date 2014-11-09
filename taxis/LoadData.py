import datetime
import Results
import Records
from Utility import *


def parse_subset(subset_str):
    """
    Parses the subset string to get the earliest and latest times to consider in the dataset.
    """
    print 'Initializing ...'
    times = subset_str.split(' ')
    first = datetime.datetime.strptime(times[0], "%Y-%m-%dT%H:%M:%S")
    last = datetime.datetime.strptime(times[1], "%Y-%m-%dT%H:%M:%S") + ONE_HOUR
    first = first.replace(minute=0, second=0)
    last = last.replace(minute=0, second=0)
    print first, last, num_hours(first, last)
    print '... finished Initializing'
    return first, last


def calculate_times(id_list, dataset):
    """
    Looks through the dataset to figure out the earliest and latest times.
    """
    print 'Initializing ...'
    firsts = []
    lasts = []
    for this_id in id_list:
        try:
            with open(dataset + '/new_' + this_id + '.txt') as f:
                lasts.append(Records.extract_time(f.readline()))
                for line in f:
                    pass
                firsts.append(Records.extract_time(line))
        except IOError:
            print 'Could not open id_file for', this_id, '.'
    first = min(firsts)
    last = max(lasts) + ONE_HOUR
    first = first.replace(minute=0, second=0)
    last = last.replace(minute=0, second=0)
    print '... finished Initializing'
    return first, last


def calculate_results(id_list, dataset, first_last):
    """
    Runs through the dataset calculating the results considering only records between the first and last times.
    """
    first, last = first_last

    results = Results.Results()

    hours = num_hours(first, last)
    if hours <= 1: # There are no results when hours = 1 because an extra hour is added.
        return results

    results.first_time = first
    results.num_uniques_over_time = [0] * hours

    for num, this_id in enumerate(id_list):
        try:
            with open(dataset + '/new_' + this_id + '.txt') as f:
                records = Records.Records()
                records.calculate_statistics(f.readlines(), first, hours)
                results.add_record(this_id, records)
                print 'Loaded ' + str(num + 1) + ' of ' + str(len(id_list))
        except IOError:
            print ('Could not open id_file for ' + this_id + '.')
    return results


def load_ids(file_name):
    """
    Loads the id_list files (eg _cabs.txt) and returns a list of all ids.
    """
    id_list = []
    with open(file_name) as f:
        for line in f.readlines():
            id_list.append(parse_value(line, 'id'))
    return id_list


def parse_ids(ids):
    """
    Parses the ids string (eg nbsd shrfs asdsds) and returns a list of all ids.
    """
    id_list = ids.split(' ')
    print id_list
    return id_list

def parse_value(line, key):
    """
    Can parse 'id' or 'updates' from an id_list file.
    """
    line = line.replace('/>', '').replace('\r\n', '')
    values = line.split(' ')[1:]
    for i in values:
        key_value = i.split('=')
        if key_value[0] == key:
            return key_value[1].replace('\"', '')