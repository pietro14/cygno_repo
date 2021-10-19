from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cygno_repo',                                            # package name
    author="Giovanni Mazzitelli",
    author_email="giovanni.mazzitelli@lnf.infn.it",
    version='0.1',                          # version
    description='Packge to hadle Cygno experimet repository',      # short description
    url='https://github.com/gmazzitelli/cygno_repo',               # package URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache2 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
    'boto3',
    'boto3sts',
    'requests',
    'pandas',
    'logging',
    'botocore',
    'requests',
    'platform',
    'optparse'
   ]

)
