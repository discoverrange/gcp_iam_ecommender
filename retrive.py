import requests
import urllib3
import json
import traceback
import json
import re
import gcsfs
import sys
import subprocess
import json
import shlex
from google.cloud import storage
from google.cloud.storage import Client

#Author discoverrange

webhook_url = ''# Paste your webhook URL 

# Send Slack notification based on the given message
def slack_notification(message):
    try:
        slack_message = {'text': message}

        http = urllib3.PoolManager()
        response=http.request('POST',
                                webhook_url,
                                body = json.dumps(slack_message),
                                headers = {'Content-Type': 'application/json'},
                                retries = False)
    except:
        traceback.print_exc()

    return True



if len(sys.argv)>=1:
    # Get Arguments
    projectname = sys.argv[1]
    print(projectname)

with open("file.txt") as file:
  for item in file:
   
    key=str(item.replace("\n", ""))

    gcs_file_system = gcsfs.GCSFileSystem(project="")#mention the project ID where the iamlogs bucket you have created
   
    get_api = json.load(gcs_file_system.open(key))
    rec=get_api["content"]["operationGroups"]
    for a in rec:
        action=a["operations"]
        for b in action: 
                act=b["action"]
                try:
                    if act == "add" :
                      print("-----------------")
                      print("Add these roles")
                      t=b["pathFilters"]["/iamPolicy/bindings/*/role"]
                      use=b["value"]
                      usr= str(use).split(':')[1] 
                      print(usr + ":" + t)
                      command_add = "gcloud projects add-iam-policy-binding "+projectname+" --member="+use+" --role="+t
                      project_output_add = subprocess.check_output(shlex.split(command_add)) 
                      print(project_output_add)
                      slack_notification('GCP_IAM_ADD! Added Roles:'+ t + ' member'+ use + ' project'  + projectname)
                except Exception as e:
                    print("skipped")
                    slack_notification('GCP_IAM!_SKIPPED_ADD in Project ' +projectname)
                try:
                    if act == "remove" :
                        print("Remove these roles")
                        mem=b["pathFilters"]["/iamPolicy/bindings/*/members/*"]
                        r=b["pathFilters"]["/iamPolicy/bindings/*/role"]
                        usr= str(mem).split(':')[1] 
                        print(usr + ":" + r)
                        command = "gcloud projects remove-iam-policy-binding "+projectname+" --member="+mem+" --role="+r 
                        project_output = subprocess.check_output(shlex.split(command)) 
                        print(project_output)   
                        print("removed")
                        slack_notification('GCP_IAM_REMOVE!'+projectname)
                        slack_notification('GCP_IAM_REMOVE! Removed Roles:'+ r +' member'+ mem + ' project'  + projectname)
                except Exception as e:
                    print("skipped removed")   
                    slack_notification('GCP_IAM_SKIPPED! '+projectname)   
    print("------------------------------")