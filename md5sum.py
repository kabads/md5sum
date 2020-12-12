from pathlib import Path
import hashlib

pathlist = Path("test").glob('**/*.txt')

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

for path in pathlist:
     hash = md5(path)
     print(path, ": ", hash)
     # TODO output file name and hash on one line to a file

