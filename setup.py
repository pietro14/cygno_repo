from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cygno',                                            # package name
    author="Giovanni Mazzitelli",
    author_email="giovanni.mazzitelli@lnf.infn.it",
    version='1.0.1',                                         # version
    description='Cygno Experiment Python Packge',            # short description
    url='https://github.com/gmazzitelli/cygno_repo',         # package URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache2 License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    scripts=['bin/cygno_repo', 'bin/cygno_runs', 'bin/cygno_his2root'],
    python_requires='>=3.5',
    install_requires=[
    'boto3',
    'boto3sts',
    'requests',
    'pandas',
    'botocore',
    'requests',
    'matplotlib',
#    'ROOT',
    'root_numpy',
    'tqdm'
   ]
)
