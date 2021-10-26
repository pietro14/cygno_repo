# CYGNO library
tools to handle cygno repository, image, ecc.

## CYGNO CLI Tools cygno_repo

* configure *oidc-agent* on your machine: https://codimd.web.cern.ch/s/SL-cWzDZB (DAQ setup, expert only https://codimd.web.cern.ch/s/_XqFfF_7V)
* example for osx

      brew tap indigo-dc/oidc-agent
      brew install oidc-agent

* install the IAM-Profile (not WLCG-Profile token) as reported in the second part of the guide https://codimd.web.cern.ch/s/SL-cWzDZB

* install python library  (https://github.com/DODAS-TS/boto3sts): 

      pip3 install -U git+https://github.com/DODAS-TS/boto3sts
      
* see https://boto3.amazonaws.com/v1/documentation/api/latest/index.html for S3 documentation

before run the script carte the iam token:

      eval `oidc-agent`
      oidc-token infncloud-iam (only first time)
 
or refresh the token
 
      eval `oidc-agent`
      oidc-gen --reauthenticate --flow device infncloud-iam (if you alrady have the token)

install the CYGNO library:

      pip install -U git+https://github.com/gmazzitelli/cygno_repo.git

usage

	Usage: cygno_repo	 [-tsv] [ls backet]
				 [put backet filename]
				 [[get backet filein] fileout]
				 [rm backet fileneme]
	
	
	Options:
	  -h, --help            	show this help message and exit
	  -t TAG, --tag=TAG     	tag where dir for data;
	  -s SESSION, --session=SESSION	token profile [infncloud-iam];
	  -v, --verbose         	verbose output;
                   
example:

      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo ls cygno-sim -t test
      2021-10-17 10:03:21  test/s3_list.py
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo put cygno-sim s3_function.py -t test
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo ls cygno-sim -t test
      2021-10-26 16:36:03  test/s3_function.py
      2021-10-17 10:03:21  test/s3_list.py
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo get cygno-sim s3_function.py -t test
      downloading file of 5.82 Kb...
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo ls cygno-sim -t test
      2021-10-26 16:36:03  test/s3_function.py
      2021-10-17 10:03:21  test/s3_list.py
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo rm cygno-sim s3_function.py -t test
      removing file of 5.82 Kb...
      removed file: s3_function.py
      Giovannis-MacBook-Air-2:script mazzitel$ cygno_repo ls cygno-sim -t test
      2021-10-17 10:03:21  test/s3_list.py
