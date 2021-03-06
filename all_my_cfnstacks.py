#!/usr/local/bin/python3

import os, sys, pprint
import Inventory_Modules
import argparse
from colorama import init,Fore,Back,Style
from botocore.exceptions import ClientError, NoCredentialsError

import logging

init()

# UsageMsg="You can provide a level to determine whether this script considers only the 'credentials' file, the 'config' file, or both."
parser = argparse.ArgumentParser(
	description="We\'re going to find all resources within any of the profiles we have access to.",
	prefix_chars='-+/')
<<<<<<< HEAD
# parser.add_argument(
# 	"-c","--creds",
# 	dest="plevel",
# 	metavar="Creds",
# 	default="1",
# 	help="Which credentials file to use for investigation.")
=======
>>>>>>> development
parser.add_argument(
	"-p","--profile",
	dest="pProfiles",
	nargs="*",
	metavar="profile to use",
	default=["all"],
	help="To specify a specific profile, use this parameter. Default will be ALL profiles, including those in ~/.aws/credentials and ~/.aws/config")
parser.add_argument(
	"-f","--fragment",
	dest="pstackfrag",
	metavar="CloudFormation stack fragment",
	default="all",
	help="String fragment of the cloudformation stack or stackset(s) you want to check for.")
parser.add_argument(
	"-s","--status",
	dest="pstatus",
	metavar="CloudFormation status",
	default="active",
	help="String that determines whether we only see 'CREATE_COMPLETE' or 'DELETE_COMPLETE' too")
parser.add_argument(
	"-r","--region",
	nargs="*",
	dest="pregion",
	metavar="region name string",
	default=["us-east-1"],
	help="String fragment of the region(s) you want to check for resources.")
parser.add_argument(
<<<<<<< HEAD
	"+delete", "+forreal",
	dest="flagDelete",
	default=False,
	action="store_const",
	const=True,
	help="Whether to delete the detectors it finds.")
=======
	"+delete","+forreal",
	dest="DeletionRun",
	const=True,
	default=False,
	action="store_const",
	help="This will delete the stacks found - without any opportunity to confirm. Be careful!!")
>>>>>>> development
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const",
	dest="loglevel",
	const=logging.INFO,
    default=logging.CRITICAL)
parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const",
	dest="loglevel",
	const=logging.WARNING)
args = parser.parse_args()

pProfiles=args.pProfiles
<<<<<<< HEAD
# plevel=args.plevel
pRegionList=args.pregion
pstackfrag=args.pstackfrag
pstatus=args.pstatus
DeletionRun=args.flagDelete
=======
pRegionList=args.pregion
pstackfrag=args.pstackfrag
pstatus=args.pstatus
verbose=args.loglevel
DeletionRun=args.DeletionRun
>>>>>>> development
logging.basicConfig(level=args.loglevel)

SkipProfiles=["default","Shared-Fid"]

##########################
ERASE_LINE = '\x1b[2K'

NumStacksFound = 0
NumRegions = 0
print()
fmt='%-20s %-15s %-15s %-50s'
print(fmt % ("Profile","Region","Stack Status","Stack Name"))
print(fmt % ("-------","------","------------","----------"))

RegionList=Inventory_Modules.get_ec2_regions(pRegionList)
ProfileList=Inventory_Modules.get_profiles(pProfiles,SkipProfiles)
# sys.exit(1)
<<<<<<< HEAD
StacksToDelete=[]
logging.warning("Searching %s profiles and %s regions" % (len(ProfileList),len(RegionList)))

=======
StacksFound=[]
>>>>>>> development
for pregion in RegionList:
	NumRegions += 1
	NumProfilesInvestigated = 0	# I only care about the last run - so I don't get profiles * regions.
	for profile in ProfileList: #Inventory_Modules.get_profiles(pProfiles,plevel,SkipProfiles):
		NumProfilesInvestigated += 1
		try:
			Output=Inventory_Modules.find_stacks(profile,pregion,pstackfrag,pstatus)

			# This is what the 'Output' dictionary looks like:
			# [{
			# 	'CreationTime': datetime.datetime(2019, 1, 9, 14, 50, 16, 110000, tzinfo=tzutc()),
			# 	'StackId': 'arn:aws:cloudformation:sa-east-1:814274863958:stack/StackSet-AWS-Landing-Zone-SharedTopic-84773a80-fdca-4043-8029-3f9247a72dec/e0054682-141d-11e9-9dd0-50a6868558c6',
			# 	'StackName': 'StackSet-AWS-Landing-Zone-SharedTopic-84773a80-fdca-4043-8029-3f9247a72dec',
			# 	'StackStatus': 'CREATE_COMPLETE',
			# 	'TemplateDescription': 'Create notification aggregation SNS topics.'
			# }]

			NumObjects=len(Output)
			# StackSets=Inventory_Modules.find_stacksets(profile,pregion,pstackfrag)
			# pprint.pprint(Stacks)
<<<<<<< HEAD
			print(ERASE_LINE,Fore.RED+"Profile: ",profile,"Region: ",pregion,"Found",NumObjects,"Stacks"+Fore.RESET,end="\r")
=======
			StackNum=len(Stacks)
			logging.warning("Profile: %s | Region: %s | Found %s Stacks", profile, pregion, StackNum )
			print(ERASE_LINE,Fore.RED+"Profile: {} Region: {} Found {} Stacks".format(profile,pregion,StackNum)+Fore.RESET,end='\r')
>>>>>>> development
		except ClientError as my_Error:
			if str(my_Error).find("AuthFailure") > 0:
				print(profile+": Authorization Failure")
		if NumObjects > 0:
			for y in range(len(Output)):
				StacksToDelete.append([profile,pregion,Output[y]['StackName']])
				"""
				The layout of this array is as follows:
					- StacksToDelete[0] = Profile
					- StacksToDelete[1] = Region
					- StacksToDelete[2] = StackName
				"""

		# 		IsDefault=Stacks['StackSummaries'][y]['IsDefault']
		# 		CIDR=Stacks['Stacks'][y]['CidrBlock']
		# 		if 'Tags' in Stacks['StackSummaries'][y]:
		# 			for z in range(len(Stacks['StackSummaries'][y]['Tags'])):
		# 				if Stacks['StackSummaries'][y]['Tags'][z]['Key']=="Name":
		# 					VpcName=Stacks['StackSummaries'][y]['Tags'][z]['Value']
		# 		else:
		# 			VpcName="No name defined"
<<<<<<< HEAD
				print(fmt % (profile,pregion,Output[y]['StackStatus'],Output[y]['StackName']))

=======
				print(fmt % (profile,pregion,StackStatus,StackName))
				NumStacksFound += 1
				StacksFound.append([profile,pregion,StackName,Stacks[y]['StackStatus']])
				"""
				StacksFound[x][0]=profile
				StacksFound[x][1]=region
				StacksFound[x][2]=Stack Name
				StacksFound[x][3]=Stack Status
				"""
>>>>>>> development
print(ERASE_LINE)
RegionSet=set([StacksToDelete[y][1] for y in range(len(StacksToDelete))])
print(Fore.RED+"Found {} Stacks across".format(len(StacksToDelete)),NumProfilesInvestigated,"profiles across",len(RegionSet),"regions"+Fore.RESET)
print()
<<<<<<< HEAD

if DeletionRun:
	for y in range(len(StacksToDelete)):
		print("Deleting stack {} in profile {} in region {}".format(StacksToDelete[y][2],StacksToDelete[y][0],StacksToDelete[y][1]))
		Response=Inventory_Modules.delete_stack(StacksToDelete[y][0],StacksToDelete[y][1],StacksToDelete[y][2])
=======
pprint.pprint(StacksFound)

if DeletionRun:
	logging.warning("Deleting %s stacks",len(StacksFound))
	for y in range(len(StacksFound)):
		print("Deleting stack {} from profile {} in region {} with status: {}".format(StacksFound[y][2],StacksFound[y][0],StacksFound[y][1],StacksFound[y][3]))
		""" This next line is BAD because it's hard-coded for GuardDuty, but we'll fix that eventually """
		if StacksFound[y][3] in ["DELETE_FAILED"]:
			response=Inventory_Modules.delete_stack(StacksFound[y][0],StacksFound[y][1],StacksFound[y][2],RetainResources=True,ResourcesToRetain=["MasterDetector"])
		else:
			response=Inventory_Modules.delete_stack(StacksFound[y][0],StacksFound[y][1],StacksFound[y][2])
print("Thanks for playing...")
>>>>>>> development
