from pathlib import Path
import hashlib
# from hexdump import hexdump
#import base64
import os
from azure.storage.blob import BlobServiceClient

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_paths(pathlist, file):
    for path in pathlist:
        # path1 = '/mnt/c/Users/adamc/PycharmProjects/md5sum/100.jpg'
        command = "md5sum --binary " + str(path.absolute()) +" | awk '{print $1}' | xxd -p -r | base64"
        # print(command)
        #a = check_output(command).strip()
        name = str(path.name)
        output = name + ": " + os.popen(command).read()
        print (output)
        file.write(output)
        #print (os.system("md5sum --binary /mnt/c/Users/adamc/PycharmProjects/md5sum/100.jpg | awk '{print $1}' | xxd -p -r | base64").strip())

def remote_check():
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "global"
    # print("\nListing containers...")

    container = blob_service_client.get_container_client(container=container_name)

    blob_list = container.list_blobs()
    count = 0
    for blob in blob_list:
        if count < 10:
            print("\t" + blob.name)
        else:
            break



# def main():
#     file = open("local-jpeg.txt", "w")
#     # pathList = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
#     pathList = Path("/mnt/c/Users/adamc/jewson-images/global/product-images/").glob('**/*.jpg')
#     file_paths(pathList, file)
#     file.close()

def main():
    remote_check()

if __name__ == '__main__':
    main()
