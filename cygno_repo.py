#!/usr/bin/env python3
#
# G. Mazzitelli and I. Abritta Febraury 2019
# Tool to Upload/Download Files into/from the Swift Cloud
# Modify by GM 2021 for S3
#
import re
import sys
import os

import numpy as np
import time
import datetime
import platform
from optparse import OptionParser

############################
def kb2valueformat(val):
    import numpy as np
    if int(val/1024./1024/1024.)>0:
        return val/1024./1024./1024., "Gb"
    if int(val/1024./1024.)>0:
        return val/1024./1024., "Mb"
    if int(val/1024.)>0:
        return val/1024., "Kb"
    return val, "byte"
############################    
def s3_backet_list(tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
    import boto3
    from boto3sts import credentials as creds
    import pandas as pd
    endpoint='https://minio.cloud.infn.it/'
    version='s3v4'
    key = tag+'/'
    if verbose: print(">> listing", tag, "on backet", bucket, "for session",  session, "\n")
    aws_session = creds.assumed_session(session)
    s3 = aws_session.client('s3', endpoint_url=endpoint,
                            config=boto3.session.Config(signature_version=version),verify=True)
    response = s3.list_objects(Bucket=bucket)['Contents']
    for i, file in enumerate(response):
        if key in str(file['Key']):
            print("{0:20s} {1:s}".format(str(file['LastModified']).split(".")[0], file['Key']))
############################    
def s3_obj_put(filename, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#uploading-files
    import boto3
    from boto3sts import credentials as creds
    import logging
    import botocore
    import requests
    import os
    #
    endpoint='https://minio.cloud.infn.it/'
    version='s3v4'
    #
    if verbose: print(">> upload", filename,"taged", tag, "on backet", bucket, "for session",  session, "\n")
    aws_session = creds.assumed_session(session)
    s3 = aws_session.client('s3', endpoint_url=endpoint, config=boto3.session.Config(signature_version=version),verify=True)

    key = tag+'/'

    # Upload the file
    
    try:
        response=s3.head_object(Bucket=bucket,Key=key+filename)
        value, unit = kb2valueformat(response['ContentLength'])
        print("The file already exists and has a dimension of {:.2f} {:s}".format(value, unit))
        #print("The file already exists and has a dimension of "+str(response['ContentLength']/1024./1024.)+' MB')
        return True, False
    
    except (botocore.exceptions.ConnectionError, requests.exceptions.ConnectionError):
        print("There was a connection error or failed")
        return False, False

    except botocore.exceptions.ClientError:
        
        if verbose: print('No file with this name was found on the cloud, it will be uploaded')
        try:
            out = key+os.path.basename(filename)
            response = s3.upload_file(filename, bucket, out)
            if verbose: print ('Uploaded file: '+out)
        except Exception as e:
            logging.error(e)
            return False, False
        return True, True
############################
def s3_obj_get(filein, fileout, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#uploading-files
    import boto3
    from boto3sts import credentials as creds
    import logging
    import botocore
    import requests
    import os
    #
    endpoint='https://minio.cloud.infn.it/'
    version='s3v4'
    #
    if verbose: print(">> get", filein, fileout,"taged", tag, "on backet", bucket, "for session",  session, "\n")
    aws_session = creds.assumed_session(session)
    s3 = aws_session.client('s3', endpoint_url=endpoint, config=boto3.session.Config(signature_version=version),verify=True)

    key = tag+'/'

    # Download the file
    
    try:
        response=s3.head_object(Bucket=bucket,Key=key+filein)
        value, unit = kb2valueformat(response['ContentLength'])
        print("downloading file of {:.2f} {:s}...".format(value, unit))    
    except (botocore.exceptions.ConnectionError, requests.exceptions.ConnectionError):
        print("There was a connection error or failed")
        return False

    except botocore.exceptions.ClientError:
        print('No file with this'+fielneme+'was found on the cloud')
        return False
    try:
        object_in = key+filein
        response = s3.download_file(bucket, object_in, fileout)
        if verbose: print ('Downloaded file: '+fileout)
        return True
    except Exception as e:
        logging.error(e)
        return False
def s3_obj_rm(filename, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html#uploading-files
    import boto3
    from boto3sts import credentials as creds
    import logging
    import botocore
    import requests
    import os
    #
    endpoint='https://minio.cloud.infn.it/'
    version='s3v4'
    #
    if verbose: print(">> get", filein, fileout,"taged", tag, "on backet", bucket, "for session",  session, "\n")
    aws_session = creds.assumed_session(session)
    s3 = aws_session.client('s3', endpoint_url=endpoint, config=boto3.session.Config(signature_version=version),verify=True)

    key = tag+'/'

    # Download the file
    
    try:
        response=s3.head_object(Bucket=bucket,Key=key+filename)
        value, unit = kb2valueformat(response['ContentLength'])
        print("removing file of {:.2f} {:s}...".format(value, unit))    
    except (botocore.exceptions.ConnectionError, requests.exceptions.ConnectionError):
        print("There was a connection error or failed")
        return False

    except botocore.exceptions.ClientError:
        print('No file with this'+fielneme+'was found on the cloud')
        return False
    try:
        object_in = key+filename
        response = s3.delete_object(Bucket=bucket,Key=object_in)
        print ('removed file: '+filename)
        return True
    except Exception as e:
        logging.error(e)
        return False
##############################
########### Main #############
##############################
def main():
    #
    # define available backet on remote repo
    #
    cygno_backet_list = ["cygnus", "cygno-data", "cygno-sim", "cygno-analysis"]
    #
    parser = OptionParser(usage='usage: %prog\t [-tsv] [ls backet]\n\t\t\t [put backet filename]\n\t\t\t [[get backet filein] fileout]\n\t\t\t [rm backet fileneme]\n')
    parser.add_option('-t','--tag', dest='tag', type='string', default='', help='tag where dir for data;');
    parser.add_option('-s','--session', dest='session', type='string', default='infncloud-iam', help='token profile [infncloud-iam];');
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output;');
    (options, args) = parser.parse_args()
    #
    if options.verbose: 
        print(">> resquested arguments:", args)
        print(">> resquested options:", options)
        if len(args)>=1:
            print(">> funcition", args[0])
        if len(args)==2:
            print(">> backet", args[1])
        if len(args)==3:
            print(">> backet", args[2])
    #       
    if len(args) < 2:
        parser.error("incorrect number of arguments")
    if not (args[1] in cygno_backet_list):
        error = "backet not availabe in cygno repo: "+str(cygno_backet_list)
        parser.error(error)
    if args[0] == 'ls':
        s3_backet_list(tag=options.tag, bucket=args[1], 
                       session=options.session, verbose=options.verbose)
    elif args[0] == 'put':
        if len(args) < 3:
            parser.error("incorrect number of arguments, no FILENAME passed")
        else:
            s3_obj_put(filename=args[2], tag=options.tag, bucket=args[1], 
                          session=options.session, verbose=options.verbose)
    elif args[0] == 'get':
        if len(args) < 3:
            parser.error("incorrect number of arguments, no FILENAME passed")
        else:
            if len(args)==4:
                fileout=args[3]
            else:
                fileout=args[2]
                
            s3_obj_get(filein=args[2], fileout=fileout, tag=options.tag, bucket=args[1], 
                          session=options.session, verbose=options.verbose)
    elif args[0] == 'rm':
        if len(args) < 3:
            parser.error("incorrect number of arguments, no FILENAME passed")
        else:
            s3_obj_rm(filename=args[2], tag=options.tag, bucket=args[1], 
                          session=options.session, verbose=options.verbose)
    elif args[0] == 'mv':
        parser.error("mouve file not yet implemented, sorry...")
    else:
        error = args[0]+" function not avaiable"
        parser.error(error)
        
if __name__ == "__main__":
    main()
