#! /usr/env/python
# xml_mapper.py
#
# Author:		David McLaren
# Description:	Maps out events for California Highway Patrol as well as
#				Southern California Edison Outages.
# ------------------------------------------------------------------------------
import arcpy
import csv
from arcpy import env
from urllib2 import urlopen
from xml.etree import ElementTree

class Mapper(object):
	""" Maps out CHP events to a point feature class.

	Attributes:
		records: Stores records of CHP incidents.
	"""
	def __init__(self):
		""" Inits Mapper with output file path and dictionary of data"""
		self.records = []


	def remove_quotes(self, text):
		""" Removes quotes from text by shearing off the first and last element
		    of a string.
		"""
		if text != None:
			if text[0:1] is '"':
				return text[1:-1]

		return text


	def read_chp_xml(self, xml_url):
		""" Reads California Highway Patrol incident xml from xml_url, storing 
			in a list.
		"""
		connection = urlopen(xml_url)
		in_xml = connection.read()
		state = ElementTree.fromstring(in_xml)
		records = []
		record = []

		# Specific to CHP
		# TODO(David) Nested for loops are bad. Change this to be more
		# efficient, possibly use generators.
		for center in state:
			rec_center = center.attrib['ID']

			for dispatch in center:
				rec_dispatch = dispatch.attrib['ID']

				for log in dispatch:
					record = [rec_center, rec_dispatch]

					record.append(log.attrib['ID'])

					log_time = self.remove_quotes(log.find('LogTime').text)
					log_type = self.remove_quotes(log.find('LogType').text)
					location = self.remove_quotes(log.find('Location').text)
					loc_desc = self.remove_quotes(log.find('LocationDesc').text)
					area = self.remove_quotes(log.find('Area').text)

					record.append(log_time)
					record.append(log_type)
					record.append(location)
					record.append(loc_desc)
					record.append(area)

					latlon = log.find('LATLON').text

					# [1:-1] Removes quotes
					(lat, lon) = latlon[1:-1].split(':')
					lat = str(lat[:2]) + '.' + str(lat[2:])
					lon = '-' + str(lon[:3]) + '.' + str(lon[3:])

					record.append(lat)
					record.append(lon)
			
					records.append(record)

		self.records = records


	def read_edison_xml(self, xml_url):
		""" Reads Southern California Edison outages xml from xml_url, storing 
			in a list.
		"""
		connection = urlopen(xml_url)
		in_xml = connection.read()
		root = ElementTree.fromstring(in_xml)
		records = []
		record = []

		# Specific to Edison
		incidents = root.find('AOC_INCIDENTS')

		for incident in incidents:
			record = []

			for node in incident:
				record.append(node.text)

			records.append(record)

		self.records = records


	def write_csv(self, out_file_name, header):
		""" Exports records to .csv file.
		"""

		with open(out_file_name, 'wb') as outf:
			writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
			writer.writerow(header)
			writer.writerows(self.records)
	

	def make_xy(self, save_location, in_table, x_coords, y_coords, sp_ref):
		""" Using ArcPy create a point shapefile.
		"""
		try:
			# Assign Variables
			out_layer = 'events'

			# Create XY Layer (this will not save it)
			arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, out_layer, sp_ref)

			# Overwrite the file no matter what
			arcpy.env.overwriteOutput = True

			# Save to layer file
			arcpy.SaveToLayerFile_management(out_layer, save_location)

		except:
			print(arcpy.GetMessages())


def main():



	# Now for Edison
	mapper.read_edison_xml('https://www.sce.com/nrc/AOC/AOC_Location_Report.xml')
	header = [
				'Incident_ID',
				'Incident_Type',
				'Fac_Job_Status_CD',
				'OAN_NO',
				'Outage_Start',
				'Version',
				'Last_Change',
				'Est_CLU',
				'Memo_Cause_CD',
				'Memo_Cause_CD_Desc',
				'Crew_Status',
				'Crew_Status_CD_Desc',
				'Result_CD',
				'Result_CD_Desc',
				'Nbr_Cust_Affected',
				'Zip_Code',
				'County_Name',
				'City_Name',
				'District_No',
				'Sector_No',
				'ERT_CD',
				'Centroid_X',
				'Centroid_Y'
			]

	mapper.write_csv('edison_output.csv', header)

	mapper.make_xy('H:/Code/chp_mapper/edison_events.lyr', 'edison_output.csv', 'Centroid_X', 'Centroid_Y', 4326)


if __name__ == '__main__':
	main()
