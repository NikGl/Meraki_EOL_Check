#######################################################################
#	Meraki EOL Check												  #
#	author: Niklas Gleich											  #
#																	  #
#######################################################################

import meraki
import json
import sys

#paste in your API access key 
accesskey="6bec40cf957de430a6f1f2baa056b99a4fac9ea0"

#initial api call
dashboard_call = meraki.DashboardAPI(api_key=accesskey, base_url='https://api.meraki.com/api/v1/',output_log=False,print_console=False)


def api_network_devices():
	#getOrganizations
	orgs = dashboard_call.organizations.getOrganizations()
	#print(json.dumps(orgs, indent=2))
	
	#getOrganizationDevices - paste in Organization ID
	org_devices = dashboard_call.organizations.getOrganizationDevices(549236)
	#print(json.dumps(org_devices, indent=2))
	device_list = []
	for device in org_devices:
		device_list.append([device["model"], device["serial"]])

	return device_list
	
def read_csv():
	#reading in csv file containing eol dates
	try:
		d = open("meraki_eol.csv")
	except:
		print("Selected File is not accessible")
		sys.exit(0)

	#Reading the whole text
	whole_text = d.read()

	#Close File
	d.close()

	#Convert Text to a list of rows
	rowlist = whole_text.split(chr(10))
	
	#Convert each Row into a seperate list item
	eol_dates = []
	for line in rowlist:
		if line:
			li = line.split(";")
			#Append model name and EoL date to List
			eol_dates.append([str(li[0]),str(li[3])])
	return eol_dates
	
def report_csv(dl, eol):
	try:
		#open in write mode so that entrys only appear in the report once and get not appended
		#report get overwritten everytime its opened again
		d = open("EOL REPORT.csv","w")
	except:
		quit()
	for device in dl:
		for data in eol:
			#if the modelname matches a model in the eol list
			if str(device[0]) == str(data[0]):
				#write modelname, serialnumber, eol date in csv file
				d.write(str(device[0])+";"+str(device[1])+";"+str(data[1])+"\n")
	d.close()
	

# MAIN 
device_list = api_network_devices()
eol_dates = read_csv()
report_csv(device_list, eol_dates)


