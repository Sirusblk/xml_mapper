#! /usr/env/python
# map_edison.py
#
# Author:		David McLaren
# Description:	Maps out events for Southern California Edison outages.
# ------------------------------------------------------------------------------
import arcpy
import csv
from arcpy import env
from urllib2 import urlopen
from xml.etree import ElementTree
from xml_mapper import Mapper

class Edison_Mapper(Mapper):
	""" Maps out Southern California Edison outages.

	Attributes:
		records: Stores records of SCE outages. (Inherited from Mapper class)
	"""
	def __init__(self, url):
		super(Edison_Mapper, self).__init__(url)


	def read_xml(self):
		""" Reads Southern California Edison outages xml from self.url, storing 
			records in a list.
		"""
		connection = urlopen(self.url)
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


def main():
	mapper = Edison_Mapper('https://www.sce.com/nrc/AOC/AOC_Location_Report.xml')
	mapper.read_xml()

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

	# 4326 is the code for WGS 1984
	mapper.make_xy('H:/Code/xml_mapper/edison_events.lyr', 'edison_output.csv', 'Centroid_X', 'Centroid_Y', 4326)


if __name__ == '__main__':
	main()
