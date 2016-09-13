#! /usr/env/python
# xml_mapper.py
#
# Author:       David McLaren
# Description:  Base Mapper Class that maps out events from xml files.
# ------------------------------------------------------------------------------
import arcpy
import csv
from abc import abstractmethod
from arcpy import env
from urllib2 import urlopen
from xml.etree import ElementTree

class Mapper(object):
    """ Maps out CHP events to a point feature class.

    Attributes:
        records: Stores records of inncident locations.
    """
    def __init__(self, layer_name, url):
        """ Inits Mapper with a layer name, an xml url, and an empty list for
            records.

        Args:
            layer_name:     Layer Name for resulting .lyr file
            url:            URL for xml file.
        """
        self.layer_name = layer_name
        self.url = url
        self.records = []


    @abstractmethod
    def read_xml(self):
        """ This is an empty function the children must implement
        """
        pass


    def write_csv(self, out_file_name, header):
        """ Exports list of records to .csv file.

        Exports Mapper records to .csv file under the given output file name.
        First line contains the header list of field names.

        Args:
            out_file_name:  Output file name to save as.
            header:         List of field names, in order.
        """

        with open(out_file_name, 'wb') as outf:
            writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            writer.writerows(self.records)


    def make_xy(self, save_location, in_table, x_coords, y_coords, sp_ref):
        """ Uses ArcPy to create a point shapefile.

        Geocodes input .csv file given the file, the save location, the x and y
        coordinate fields, and lastly the spacial reference of the coordinates
        (very important). Really just a wrapper for ArcPy calls to create the
        data and then save it to a file.

        Args:
            save_location:  Actual file path name to save to. Ends in .lyr
            in_table:       Tabular input .csv file. (Other formats supported)
            x_coords:       Field name for X-Coordinates
            y_coords:       Field name for Y-Coordinates
            sp_ref:         Spacial Reference by name or code.

        Returns:
            Nothing is returned, .lyr file is created.
        """
        try:
            # Assign Variables
            out_layer = self.layer_name

            # Create XY Layer (this will not save it)
            arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, out_layer, sp_ref)

            # Overwrite the file no matter what
            arcpy.env.overwriteOutput = True

            # Save to layer file
            arcpy.SaveToLayerFile_management(out_layer, save_location)

        except:
            # Any errors, push those out
            print(arcpy.GetMessages())


def main():
    pass


if __name__ == '__main__':
    main()
