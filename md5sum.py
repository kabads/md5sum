import hashlib
import os
from azure.storage.blob import BlobServiceClient
from os import sys
import binascii
import argparse
from pathlib import Path


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remote_md5_check(connection_str, file):
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
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
    for path in pathlist:
        # As I can get the md5sum straight from Azure - I don't need this weird hex base64 thing.
        # command = "md5sum --binary " + str(path.absolute()) +" | awk '{print $1}' | xxd -p -r | base64"
        name = str(path.name)
        hash_calc = md5(path)
        # This output used the old version which issued a bash command:
        # output = name + ": " + os.popen(command).read()
        # This output outputs the pure python method
        output = name + ": " + hash_calc +"\n"
        print (output)
        file.write(output)


def get_local_image_checksums(filename="20201217_md5_local_jpg.txt"):
    file = open(filename, "w")
    # The below path is for windows:
    # pathlist = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
    # This path is for linux:
    pathlist = Path("/mnt/c/Users/adamc/jewson-images/global/product-images/").glob('**/*.jpg')
    local_md5_check(pathlist, file)
    file.close()


def get_local_doc_checksums(filename='20201217_md5_local_pdf_test.txt'):
    file = open(filename, "w")
    # pathlist = Path("C:/Users/adamc/jewson-images/global/product-docs").glob('**/*.pdf')
    pathlist = Path("/mnt/c/Users/adamc/jewson-images/global/product-docs/").glob('**/*.pdf')
    local_md5_check(pathlist, file)
    file.close()


def get_remote_checksums(filename='20201217_md5_remote.txt'):
    try:
        CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        file = open(filename, "w")
        remote_md5_check(CONNECTION_STRING, file)
        file.close()
    except KeyError:
        print("AZURE_STORAGE_CONNECTION_STRING must be set.")
        sys.exit(1)


def compare():
    source_file = open('20201216_md5_local_jpg.txt', 'r')
    target_file = open('20201216_md5_remote.txt', 'r')

def main():
    parser = argparse.ArgumentParser()
    requiredlocation = parser.add_argument_group('required location arguments')
    requiredlocation.add_argument("-l", "--location", required=True, choices=["localimages", "localdocs", "remote"],
                       dest = 'destination',
                       help="Where do you wish to get the checksums? Choose ONE of the options.")
    parser.add_argument("-f", "--filename",
                        help="file to write checksums to")
    args = parser.parse_args()
    if args.filename:
        if args.destination == 'localimages':
            get_local_image_checksums(args.filename)
        elif args.destination == 'localdocs':
            get_local_doc_checksums(args.filename)
        elif args.destination == 'remote':
            get_remote_checksums(args.filename)
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
