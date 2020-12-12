from pathlib import Path
import hashlib
from hexdump import hexdump
import base64

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_paths(pathlist, file):
    count = 0
    for path in pathlist:
        hash = md5(path)
        hash_hexdump = hexdump(hash.encode())
        ascii_hash = hash_hexdump.encode('ascii')
        base64_hash_bytes = base64.b64encode(ascii_hash)
        base64_hash_message = base64_hash_bytes.decode('ascii')
        print (base64_hash_message)
        # print(path.name, ": ", base64.b64encode((hexdump(hash.encode()))))
        # output = str(path.name) + ": " + hash + "\n"
        # file.write(output)
        if count > 10:
            break
        else:
            count = count + 1
def main():
    file = open("local-jpeg.txt", "w")
    pathList = Path("C:/Users/adamc/jewson-images/global/product-images").glob('**/*.jpg')
    file_paths(pathList, file)
    file.close()

if __name__ == '__main__':
    main()