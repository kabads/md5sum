import os

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
         print(os.path.join(directory, filename))
        continue
    else:
        continue
