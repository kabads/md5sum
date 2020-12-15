from pathlib import Path
import hashlib
import os
from azure.storage.blob import BlobServiceClient
from os import sys
import base64
import binascii

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

# def main():
#     file = open("md5_local_jpeg.txt", "w")
#     # The below path is for windows:
#     # pathList = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
#     # This path is for linux:
#     pathlist = Path("/mnt/c/Users/adamc/jewson-images/global/product-images/").glob('**/*.jpg')
#     local_md5_check(pathlist, file)
#     file.close()


# def main():
#     file = open("md5_local_pdf.txt", "w")
#     # pathList = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
#     pathList = Path("/mnt/c/Users/adamc/jewson-images/global/product-docs/").glob('**/*.pdf')
#     file_paths(pathList, file)
#     file.close()


def main():
    try:
        CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        file = open("md5_remote.txt", "w")
        remote_md5_check(CONNECTION_STRING, file)
        file.close()
    except KeyError:
        print("AZURE_STORAGE_CONNECTION_STRING must be set.")
        sys.exit(1)

if __name__ == '__main__':
    main()
