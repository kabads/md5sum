from pathlib import Path
import hashlib
import os
from azure.storage.blob import BlobServiceClient
from os import sys

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_paths(pathlist, file):
    for path in pathlist:
        command = "md5sum --binary " + str(path.absolute()) +" | awk '{print $1}' | xxd -p -r | base64"
        name = str(path.name)
        output = name + ": " + os.popen(command).read()
        print (output)
        file.write(output)

def remote_check(connection_str):
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)
    container_name = "global"
    container = blob_service_client.get_container_client(container=container_name)

    blob_list = container.list_blobs()
    count = 0
    for blob in blob_list:
        if count < 10:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob)
            a = blob_client.get_blob_properties()
            # print(a.metadata.keys())
            print(a.content_settings.content_md5)
            print("Blob name: " + str(blob_client.blob_name))
            # print(blob.get_blob_properties(container_name, blob.name))
            count = count + 1
        else:
            break


# def main():
#     file = open("local-jpeg.txt", "w")
#     # pathList = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
#     pathList = Path("/mnt/c/Users/adamc/jewson-images/global/product-images/").glob('**/*.jpg')
#     file_paths(pathList, file)
#     file.close()


def main():
    try:
        CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        remote_check(CONNECTION_STRING)
    except KeyError:
        print("AZURE_STORAGE_CONNECTION_STRING must be set.")
        sys.exit(1)

if __name__ == '__main__':
    main()
