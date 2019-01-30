#!/usr/local/bin/python3

import os, sys, pprint, argparse
# from sty import
import Inventory_Modules
import boto3, logging
from colorama import init,Fore,Back,Style
from botocore.exceptions import ClientError, NoCredentialsError

init()

parser = argparse.ArgumentParser(
	description="We\'re going to find all resources within any of the profiles we have access to.",
	prefix_chars='-+/')
parser.add_argument(
	"-p","--profile",
	dest="pProfile",
	metavar="Single Master profile to use",
	default="all",
	help="To specify a specific profile, use this parameter. There is no default for this")
parser.add_argument(
	"-r","--region",
	nargs="*",
	dest="pRegion",
	metavar="region name string",
	default=["us-east-1"],
	help="String fragment of the region(s) you want to check for resources.")
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const",
	dest="loglevel",
	const=logging.DEBUG,
    default=logging.CRITICAL)
parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const",
	dest="loglevel",
	const=logging.INFO)

args = parser.parse_args()

pProfile=args.pProfile
pRegionList=args.pRegion
pService=args.pService
pCommand=args.pCommand
logging.basicConfig(level=args.loglevel)
# RegionList=[]

# if pRegionList

# SkipProfiles=["default"]
SkipProfiles=["default","Shared-Fid"]

##########################
ERASE_LINE = '\x1b[2K'

# Find all stacksets in this account
RegionList=Inventory_Modules.get_ec2_regions(pRegionList)
ChildAccounts=Inventory_Modules.find_child_accounts2(pProfile)
all_responses=[]

command_to_run='client_aws.list_roles()'
region='us-east-1'

for account in ChildAccounts:
	# for region in RegionList:
	try:
		sts_session = boto3.Session(profile_name=pProfile)
		sts_client = sts_session.client('sts',region_name=region)
		role_arn = "arn:aws:iam::{}:role/AWSCloudFormationStackSetExecutionRole".format(account['AccountId'])
		account_credentials = sts_client.assume_role(
			RoleArn=role_arn,
			RoleSessionName="IAMTestScript")['Credentials']
		session_aws=boto3.Session(
			aws_access_key_id=account_credentials['AccessKeyId'],	aws_secret_access_key=account_credentials['SecretAccessKey'], aws_session_token=account_credentials['SessionToken'],
			region_name=region)
		client_aws=session_aws.client('iam')
		logging.warning("Command to be run: %s on account: %s" % (command_to_run,account['AccountId']))
		response=eval(command_to_run)
		all_responses.append(response['Roles'])
		theresmore=(response['IsTruncated']==True)
		logging.warning("There's more?: %s" % (theresmore))
		while theresmore:
			command_to_run='client_aws.list_roles('+'Marker='+response['Marker']+')'
			response=eval(command_to_run)
			all_responses.append(response['Roles'])
			theresmore=(response['IsTruncated']==True)

	except ClientError as my_Error:
		if str(my_Error).find("AuthFailure") > 0:
			print(profile+": Authorization Failure")

# pprint.pprint(all_responses)
# pprint.pprint(response)
ExecutionRoleCount=0
for response in all_responses:
	print("**** Next account ****")
	# print(type(response))
	for i in range(len(response)):
		if response[i]['RoleName'] == 'AWSCloudFormationStackSetExecutionRole':
			print("Account: {} | RoleName {}".format(response[i]['Arn'][13:25],response[i]['RoleName']))
			pprint.pprint(response[i]['AssumeRolePolicyDocument'])
			ExecutionRoleCount+=1
			print()

print("There were {} accounts in Child Accounts".format(len(ChildAccounts)))
print("There were {} roles in the all_responses list".format(ExecutionRoleCount))
