from pathlib import Path
import hashlib


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def file_paths(pathlist, file):
    for path in pathlist:
        hash = md5(path)
        print(path, ": ", hash)
        output = str(path) + ": " + hash + "\n"
        file.write(output)

def main():
    file = open("local.txt", "w")
    pathList = Path("C:/Users/adamc/j").glob('**/*.txt')
    file_paths(pathList, file)
    file.close()

if __name__ == '__main__':
    main()