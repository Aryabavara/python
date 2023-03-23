import psycopg2
import re
from python_terraform import *
import subprocess
from subprocess import PIPE, Popen, check_output
import logging
import os
import json
from pprint import pprint
import time
import onetimepad
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import logging
import os
from google.cloud import storage

# function to split


def result_split(num):
    cidr_ranges = (num.split(','))
    str = ""
    for i in range(len(cidr_ranges)):
        str = str + '"' + cidr_ranges[i] + '",'
    cidr_out = str[:-1]
    return cidr_out


def tf_pull(path, tf_bucket_name):
    """Downloads a blob from the bucket."""
    bucket_name = tf_bucket_name
    source_blob_name = "terraform/state/{path}/default.tfstate".format(
        path=path)
    destination_file_name = "./{path}/{path}.tfstate".format(path=path)
    path_to_service_account = "/home/apton/Downloads/training-devops-326304-8e9434142607.json"
    storage_client = storage.Client.from_service_account_json(
        path_to_service_account)
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def init_func(path, tf_bucket_name):
    cmd = ["terraform", "-chdir={path}".format(
        path=path), "init", '-backend-config=bucket='+tf_bucket_name+'']
    subprocess.run(cmd)
    return{"#################.....init_completed......############"}


def destroy_func(path, newtwork_values):
    tf_destroy = ["terraform", "-chdir={path}".format(path=path), "destroy", ]
    tf_destroy.extend(newtwork_values)
    subprocess.run(tf_destroy)
    return{"#################.....destroy_completed......############"}


####################################################################################################################################
def main():
    conn = psycopg2.connect(
        database="apton_one",
        user="postgres",
        password="myPassword",
        host="localhost",
        port="5432"
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute(
        '''SELECT * FROM "Network"''')   # we have to change course_id to status check

    # Fetching 1st row from the table
    result = cursor.fetchone()

    status = (result[3])
    print("***********************************", status)
    if(status == -3):
        pass
    else:
        sys.exit()

    cursor.execute(
        '''SELECT * FROM "Gcp" ''')   # we have to change course_id to status check

    result1 = cursor.fetchone()
    id = result[0]
    NW_data = (result[4])
    credentials = (result1[3])

    print("******************FIRSTONE---ROW---*****************", NW_data)
    print("******************---ROW---*****************", credentials)

    vpc_name = NW_data["vpc_name"]
    region = NW_data["region"]
    project = NW_data["project_id"]
    subnet_region_1 = NW_data["subnet_region"]
    private_subnet_cidr_1 = NW_data["private_subnet_cidr"]
    public_subnet_cidr_1 = NW_data["public_subnet_cidr"]
    sub1_secondaryip_service_range = NW_data["sub1_secondaryip_service_range"]
    sub1_secondaryip_pod = NW_data["sub1_secondaryip_pod"]
    sub2_secondaryip_service_range = NW_data["sub2_secondaryip_service_range"]
    sub2_secondaryip_pod = NW_data["sub2_secondaryip_pod"]
    service_account = NW_data["service_account"]
    public_vm_discription = NW_data["public_vm_discription"]
    vpn_vm_type = NW_data["vpn_vm_type"]
    public_vm_zone = NW_data["public_vm_zone"]
    vm_disk_size = NW_data["vm_disk_size"]
    username = NW_data["username"]
    public_key_path = NW_data["public_key_path"]
    test_network_vpc_vpn_staticip = NW_data["test_network_vpc_vpn_staticip"]
    tf_bucket_name = "apton1-bucket" + project + vpc_name

    private_subnet_cidr = '['+result_split(private_subnet_cidr_1)+']'
    public_subnet_cidr = '['+result_split(public_subnet_cidr_1) + ']'
    subnet_region = '['+'"'+subnet_region_1+'"'+']'

    print("private_subnet_cidr range ----------------->", private_subnet_cidr)
    print("public_subnet_cidr range ----------------->", public_subnet_cidr)
    print("sub1_secondaryip_service_range range ----------------->",
          sub1_secondaryip_service_range)
    print("sub1_secondaryip_pod range ----------------->", sub1_secondaryip_pod)
    print("sub2_secondaryip_service_range range ----------------->",
          sub2_secondaryip_service_range)
    print("sub2_secondaryip_pod range ----------------->", sub2_secondaryip_pod)

    os.environ["GOOGLE_CREDENTIALS"] = str(json.dumps(credentials))

    newtwork_values = {
        'nat': ['-var=project='+project+'', '-var=region='+region+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")),  "-auto-approve"],
        'router': ['-var=project='+project+'', '-var=region='+region+'', '-var=vpc_name='+vpc_name+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), "-auto-approve"],
        'static': ['-var=project='+project+'', '-var=region='+region+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), "-auto-approve"],
        'instance': ['-var=project='+project+'', '-var=region='+region+'', '-var=vpc_name='+vpc_name+'', '-var=service_account='+service_account+'', '-var=external_ip='+test_network_vpc_vpn_staticip+'', '-var=public_vm_discription='+public_vm_discription+'', '-var=public_key_path='+public_key_path+'', '-var=username='+username+'', '-var=public_vm_zone='+public_vm_zone+'',  '-var=vm_disk_size='+vm_disk_size+'', '-var=vpn_vm_type='+vpn_vm_type+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), "-auto-approve"],
        'firewall': ['-var=project='+project+'', '-var=region='+region+'', '-var=vpc_name='+vpc_name+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), "-auto-approve"],
        'vpc': ['-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), '-var=project='+project+'', '-var=region='+region+'', '-var=subnet_region='+subnet_region+'', '-var=vpc_name='+vpc_name+'', '-var=private_subnet_cidr='+private_subnet_cidr+'', '-var=public_subnet_cidr='+public_subnet_cidr+'', '-var=sub1_secondaryip_service_range='+sub1_secondaryip_service_range+'', '-var=sub1_secondaryip_pod='+sub1_secondaryip_pod+'', '-var=sub2_secondaryip_service_range='+sub2_secondaryip_service_range+'', '-var=sub2_secondaryip_pod='+sub2_secondaryip_pod+'', "-auto-approve"],
        'jenkins': ['-var=project='+project+'', '-var=credentials={}'.format(os.environ.get("GOOGLE_CREDENTIALS")), '-var=region='+region+'', '-var=public_vm_zone='+public_vm_zone+'', '-var=public_key_path='+public_key_path+'', '-var=service_account='+service_account+'', '-var=username='+username+'', '-var=vpc_name='+vpc_name+'', "-auto-approve"]
    }

    pprint(tf_pull('instance', tf_bucket_name))
    pprint(init_func('./instance', tf_bucket_name))
    pprint(destroy_func('./instance', newtwork_values['instance']))
    print("*****************-------------------INSTANCE---Destroyed-----------------******************************")

    pprint(tf_pull('router', tf_bucket_name))
    pprint(init_func('./router', tf_bucket_name))
    pprint(destroy_func('./router', newtwork_values['router']))
    print("****************---------------------ROUTER-destroyed------------------********************************")

    pprint(tf_pull('static', tf_bucket_name))
    pprint(init_func('./static', tf_bucket_name))
    pprint(destroy_func('./static', newtwork_values['static']))
    print("*****************-------------------STATIC-IP---Destroyed--------------********************************")

    pprint(tf_pull('firewall', tf_bucket_name))
    pprint(init_func('./firewall', tf_bucket_name))
    pprint(destroy_func('./firewall', newtwork_values['firewall']))
    print("******************------------------firewall---Destroyed-------------------****************************")

    pprint(tf_pull('jenkins-terraform',tf_bucket_name))
    pprint(init_func('./jenkins-terraform','tf_func'))
    pprint(destroy_func('/jenkins','tf_func',newtwork_values['jenkins']))
    print("******************------------------jenkins---Destroyed-------------------****************************")

    pprint(tf_pull('vpc', tf_bucket_name))
    pprint(init_func('./vpc', tf_bucket_name))
    pprint(destroy_func('./vpc', newtwork_values['vpc']))
    print("*****************------------------VPC------destroyed--------------------*****************************")
    cursor.execute(
        '''UPDATE "Network" SET status = 2 WHERE id_={}'''.format(id))


if __name__ == "__main__":
    main()
