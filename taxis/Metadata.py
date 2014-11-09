#!/usr/bin/env python

import xml.etree.ElementTree as Xml
import os
import urllib2


class Metadata():
    """
    Class which is responsible for loading and parsing Crawdad Metadata files
    """
    def __init__(self, file_path):
        self.dataset = None
        self._read_data(file_path)

    def _read_data(self, file_path):
        """
        Reads in Crawdad Metadata, in XML format
        """
        try:
            metadata_tree = Xml.parse(file_path)
            self.dataset = metadata_tree.getroot()
        except IOError:
            print("Metadata file not found!")

    def quick_parse(self):
        """
        Returns some simple information about the dataset
        """
        return {"title": self.dataset.find("./dataset/dataname").text,
                "modified":  self.dataset.find("./dataset/lastmodified").text,
                "summary": self.dataset.find("./dataset/oneline").text,
                "long_desc": self.dataset.find("./dataset/environment").text}

    def get_title(self):
        """
        Returns just the title of the dataset
        """
        return self.dataset.find("./dataset/dataname").text

    def get_url(self):
        """
        Gets the URL of the datasets
        """
        return {"size": self.dataset.find("./dataset/traceset/url").get("size"),
                "type": self.dataset.find("./dataset/traceset/url").get("type"),
                "md5sum": self.dataset.find("./dataset/traceset/url").get("md5"),
                "url": self.dataset.find("./dataset/traceset/url").text}

# To debug this class, run it directly:
if __name__ == "__main__":
    meta_data = Metadata(raw_input("Metadata XML path: "))
    parsed_data = meta_data.quick_parse()
    print parsed_data
    url_data = meta_data.get_url()
    print url_data


# Called by Main.py
def process_meta(arguments):
    """
    Processes the meta data, offering to download it.
    """
    print "\n\n\n"
    try:
        meta_data = Metadata(arguments)
        parsed_data = meta_data.quick_parse()
        print "Title: " + parsed_data["title"]
        print "Summary: " + parsed_data["summary"]
        print "Modified: " + parsed_data["modified"]
        url_data = meta_data.get_url()
        if raw_input("Attempt data download (" + url_data["size"] + " as " + url_data[
            "type"] + ")? (y/n) ") == "y":
            try:
                # First get the download store - if it doesn't exist, create it.
                output_directory = raw_input("Local Crawdad trace store location: ")
                output_filename = url_data["url"].rsplit("/", 1)
                if not os.path.exists(output_directory+output_filename[0]):
                    os.makedirs(output_directory+output_filename[0])

                # Then build the full URL:
                full_url = "http://uk.crawdad.org" + url_data["url"]

                # Now set up the auth handler, for Crawdad's HTTP Authentication:
                http_password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
                http_password_manager.add_password(None, full_url, raw_input("Crawdad Username: "),raw_input("Crawdad Password: "))
                http_auth_handler = urllib2.HTTPBasicAuthHandler(http_password_manager)
                http_opener = urllib2.build_opener(http_auth_handler)
                urllib2.install_opener(http_opener)

                # Then open the remote file, and write it to the download store.
                print "Downloading - this may take some time!"
                remote_file_handle = urllib2.urlopen(full_url)
                with open((output_directory+output_filename[0] + "/" + output_filename[1]), "wb") as local_file:
                    local_file.write(remote_file_handle.read())
            except urllib2.HTTPError, e:
                print "Download failed due to HTTP error ", e.code
            except urllib2.URLError, e:
                print "Download failed because of URL error: ", e.reason
    except (ValueError, AttributeError):
        print 'Error with Metadata. Try again'