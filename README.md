# md5sum.py

This set of scripts computes and writes to a file the md5sums for files locally. 

## Installation
Install all the libraries required (in `requirements.txt`):

`pip install -r requirements.txt`

Ensure that the environment variable `AZURE_STORAGE_CONNECTION_STRING` is set to allow authentication. This can be obtained from the Azure Storage Container.

Ensure that authentication works for Azure  CLI with `az login`.

## Execution

usage: md5sum.py [-h] -l {localimages,localdocs,remote} [-f FILENAME]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --filename FILENAME
                            file to write checksums to
    
    required location arguments:
      -l {localimages,localdocs,remote}, --location {localimages,localdocs,remote}
                            Where do you wish to get the checksums? Choose ONE of
                            the options.