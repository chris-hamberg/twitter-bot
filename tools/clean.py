import shutil
import os


def scrub():
    for root, directories, files in os.walk(os.getcwd()):
        for directory in directories:
            if "__pycache__" in directory:
                shutil.rmtree(os.path.join(root, directory))
        #for file in files:
            #if "data.db" in file:
            #    os.remove(os.path.join(root, file))
            #elif "dat.log" in file:
            #    os.remove(os.path.join(root, file))


if __name__ == "__main__":
    scrub()
