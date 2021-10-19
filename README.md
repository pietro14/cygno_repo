# cygno_repo
tools to handle cygno repository
* configure *oidc-agent* on your machine: https://codimd.web.cern.ch/s/SL-cWzDZB (DAQ setup, expert only https://codimd.web.cern.ch/s/_XqFfF_7V)
* example for osx

      brew tap indigo-dc/oidc-agent
      brew install oidc-agent

* and then install the IAM-Profile (not WLCG-Profile token) as reported in the second part of the guide https://codimd.web.cern.ch/s/SL-cWzDZB

* installa python library  (raw example https://github.com/DODAS-TS/boto3sts): 

      pip3 install -U git+https://github.com/DODAS-TS/boto3sts
      
* see https://boto3.amazonaws.com/v1/documentation/api/latest/index.html for S3 documentation

before run the script rember to run:

      eval `oidc-agent`
      oidc-token infncloud-iam
 
 and eventualy refresh the token
 
      oidc-gen --reauthenticate --flow device infncloud-iam
