#!/bin/bash

declare -a AllProfiles

region=${1-"us-east-1"}

echo "Gathering profiles..."
AllProfiles=( $(./AllProfiles.sh ProfileNameOnly | awk '{print $1}') )

format='%-20s %-8s %-25s %-50s %-10s %-15s \n'

echo "Outputting all EC2 instances from all profiles"

printf "$format" "Profile" "Region" "Instance Name" "Public DNS Name" "State" "Instance ID"
printf "$format" "-------" "------" "-------------" "---------------" "-----" "-----------"
for profile in ${AllProfiles[@]}; do
	aws ec2 describe-instances --output text --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`]|[0].Value,PublicDnsName,State.Name,InstanceId]' --profile $profile --region $region | awk -F $"\t" -v rgn=${region} -v var=${profile} -v fmt="${format}" '{printf fmt,var,rgn,$1,$2,$3,$4}'
done

echo
exit 0
