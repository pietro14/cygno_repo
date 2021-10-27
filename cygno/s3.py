#
################## General TOOL for S3 ##############
#
        
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

def root_file(run, tag='LAB', posix=False, verbose=False):
    if posix:
        BASE_URL  = "/workarea/cloud-storage/cygno-data/"
        if run <= 4504:
            BASE_URL  = "/workarea/cloud-storage/cygno/Data/"
    else:
        BASE_URL  = "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygno-data/"
        if run <= 4504:
            BASE_URL  = "https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygnus/Data/"
    
    file_root = (tag+'/histograms_Run%05d.root' % run)
    if verbose: print(BASE_URL+file_root)
    return BASE_URL+file_root


def backet_list(tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
    import boto3
    from boto3sts import credentials as creds

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
            print("{0:20s} {1:s}".format(str(file['LastModified']).split(".")[0].split("+")[0], file['Key']))

def obj_put(filename, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
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

def obj_get(filein, fileout, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
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

def obj_rm(filename, tag, bucket='cygno-sim', session="infncloud-iam", verbose=False):
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