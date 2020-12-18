import hashlib
import os
from azure.storage.blob import BlobServiceClient
from os import sys
import binascii
import argparse
from pathlib import Path


def md5(fname):
    '''
    A simple function that accepts a file, and returns the md5 hash for it. 
    '''
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remote_md5_check(connection_str, file):
    '''
    Accepts a connection string to Azure and a filename parameter. Creates a BlobServiceClient
    object which provides access to the get_container_client function (a container object). 
    Once we have a container object, we can create a blob_list, listing all the blobs in that 
    container. 

    Once we have a blob_list, we can iterate through it and get the blob properties. 

    This function checks if the content_md5 property is set (it's not mandatory). If it is not
    set, then we write that to a file. 

    Once we have the content_md5 property, we can write that, along with the filename to the
    file.  
    '''
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    # TODO Accept the container name as a parameter 
    container_name = "global"
    container = blob_service_client.get_container_client(container=container_name)

    blob_list = container.list_blobs()
    for blob in blob_list:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob)
        a = blob_client.get_blob_properties()
        print("Name: " + a.name)
        b = a.content_settings.content_md5
        if b != None:
            print("B: " + str(b))
            remote_md5 = binascii.hexlify(b)
            output = a.name.split('/')[-1] + ": " + str(remote_md5.decode("utf-8")) + "\n"
            print(output)
        else:
            output = a.name.split('/')[-1] + " Did not have an md5sum." + "\n"
            print(output)
        file.write(output)


def local_md5_check(pathlist, file):
    '''
    Accepts an iterable pathlist object and filename to write out to. Passes the path to the 
    md5function. Once that is calculated, everything is written to the file. 
    '''
    for path in pathlist:
        name = str(path.name)
        hash_calc = md5(path)
        output = name + ": " + hash_calc +"\n"
        print (output)
        file.write(output)


def get_local_image_checksums(filename="20201217_md5_local_jpg.txt"):
    '''
    accepts an optional filename parameter and passes an iterable pathlist to the local_md5_check
    function.  
    '''
    file = open(filename, "w")
    # The below path is for windows:
    pathlist = Path("C:/Users/A845740/jewson-images/global/product-images").glob('**/*.jpg')
    # This path is for linux:
    # pathlist = Path("/mnt/c/Users/adamc/jewson-images/global/product-images/").glob('**/*.jpg')
    local_md5_check(pathlist, file)
    file.close()


def get_local_doc_checksums(filename='20201217_md5_local_pdf_test.txt'):
    '''
    This function accepts an optional output filename. 

    It creates a pathlist object which is an iterable list of files for a filesystem hierarchy.
    That hierarchy is passed to local_md5_check function. 
    '''
    file = open(filename, "w")
    pathlist = Path("C:/Users/A8455740/jewson-images/global/product-docs").glob('**/*.pdf')
    # pathlist = Path("/mnt/c/Users/adamc/jewson-images/global/product-docs/").glob('**/*.pdf')
    local_md5_check(pathlist, file)
    file.close()


def get_remote_checksums(filename='20201217_md5_remote.txt'):
    '''
    This function accepts an option filename parameter as the output file. 

    It uses an ENVIRONMENT VARIABLE to connect and then calls remote_md5_check with the output file
    and the connection string. If the connection string is not set it exits. 
    ''''
    try:
        CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        file = open(filename, "w")
        remote_md5_check(CONNECTION_STRING, file)
        file.close()
    except KeyError:
        print("AZURE_STORAGE_CONNECTION_STRING must be set.")
        sys.exit(1)


def compare():
    '''
    This is the stub of a function that will do the comparison in the future. It currently does nothing. 
    '''
    source_file = open('20201216_md5_local_jpg.txt', 'r')
    target_file = open('20201216_md5_remote.txt', 'r')

def main():
    '''
    Takes in parameters from the command line (see documentation) and then goes 
    to function that handles that location [localimages, localdocs, remote].

    The functions write to a file, so nothing is returned. 
    '''
    parser = argparse.ArgumentParser()
    requiredlocation = parser.add_argument_group('required location arguments')
    requiredlocation.add_argument("-l", "--location", required=True, choices=["localimages", "localdocs", "remote"],
                       dest = 'destination',
                       help="Where do you wish to get the checksums? Choose ONE of the options.")
    parser.add_argument("-f", "--outfile",
                        help="file to write checksums to")
    args = parser.parse_args()
    
    if args.outfile:
        if args.destination == 'localimages':
            get_local_image_checksums(args.outfile)
        elif args.destination == 'localdocs':
            get_local_doc_checksums(args.outfile)
        elif args.destination == 'remote':
            get_remote_checksums(args.outfile)
    else:
        destination = args.destination
        if destination == 'localimages':
            get_local_image_checksums(args.filename)
        if destination == 'localdocs':
            get_local_doc_checksums()
        if destination == 'remote':
            get_remote_checksums()


if __name__ == '__main__':
    main()
