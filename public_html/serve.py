import sys
import os
from zipfile import ZipFile, BadZipFile
from search_directories import search_directories
from search_directories import log_openable_files
import grp
import pwd

USER = "root"
UID = pwd.getpwnam(USER).pw_uid
GID = grp.getgrnam(USER).gr_gid
ZIP_EXT = '.zip'

def unzip_directories(INPUT_DIR, OUTPUT_DIR, LOG_DIR, ALL_ZIPS_LOG, UNZIPPED_LOG, OPENABABLE_LOG):

    # do setup
    setup(INPUT_DIR, OUTPUT_DIR, LOG_DIR, ALL_ZIPS_LOG, UNZIPPED_LOG, OPENABLE_LOG)

    # get list of unzipped
    all = getLogged(ALL_ZIPS_LOG)
    unzipped = getLogged(UNZIPPED_LOG)

    zips = os.listdir(INPUT_DIR)
    zips.sort()

    logZips(ALL_ZIPS_LOG, zips, all)

    f = open(UNZIPPED_LOG, "a")
    new_unzipped = []
    for z in zips:
        if not z.endswith(ZIP_EXT):
            continue
        name = z[:-4]
        if name in unzipped:
            continue
        createDirectory(name)
        os.chdir(name)
        try:
            with ZipFile(INPUT_DIR + z) as item:
                try:
                    item.extractall()
                    unzipped.append(name)
                    new_unzipped.append(name)
                    f.write(name + "\n")
                    print(name)
                except RuntimeError as e:
                    print(z)
                    print(e)
        except BadZipFile as e:
            print(z)
            print(e)
        os.chdir(OUTPUT_DIR)

    f.close()


def setup(INPUT_DIR, OUTPUT_DIR, LOG_DIR, ALL_ZIPS_LOG, UNZIPPED_LOG, OPENABLE_LOG):
    createDirectory(OUTPUT_DIR)
    createDirectory(LOG_DIR)
    
    if (not directoryExists(INPUT_DIR)):
        print("Can't evaluate because directory is missing")

    createFile(ALL_ZIPS_LOG)
    createFile(UNZIPPED_LOG)
    createFile(OPENABLE_LOG)

def logZips(log_file, new_zips, existing_zips):
    f = open(log_file, "a")
    for i in new_zips:
        name = i[:-4]
        if not (name in existing_zips):
            f.write(name + "\n")
    f.close()

def getLogged(log_file):
    f = open(log_file, "r")
    lines = [l.strip() for l in f.readlines()]
    return lines

def createDirectory(dir):
    if not directoryExists(dir):
        os.mkdir(dir, 0o755)
        os.chown(dir, UID, GID)

def createFile(file):
    if not fileExists(file):
        f = open(file, "w")
        f.close()

def directoryExists(dir):
    return os.path.isdir(dir)

def fileExists(file):
    return os.path.isfile(file) 

if __name__ == "__main__":
    args = sys.argv[1:] # python3 serve.py /var/www/html/kits/ /var/www/html/ /var/www/logs/
    INPUT_DIR = '/var/www/html/kits/' # location of zip files
    OUTPUT_DIR = '/var/www/html/' # unzip location
    LOG_DIR = '/var/www/logs/' # log directory
    ALL_ZIPS_LOG = LOG_DIR + 'all_zips.txt'
    UNZIPPED_LOG = LOG_DIR + 'unzipped.txt'
    OPENABLE_LOG = LOG_DIR + 'openable_pages.txt'

    unzip_directories(INPUT_DIR, OUTPUT_DIR, LOG_DIR, ALL_ZIPS_LOG, UNZIPPED_LOG, OPENABLE_LOG)
