#!/usr/bin/env python3
import os
import grp
import pwd
import mmap
from zipfile import ZipFile, BadZipFile
from tempfile import mkstemp
from shutil import move, copymode

ext = '.zip'
input_dir = '/var/www/html/kits/' # location of zip files
output_dir = '/var/www/html/' # unzip location
log_file = 'log.txt'
output_dir_exists = os.path.isdir(output_dir)
user = "root"

# get uid/gid for user to chown
uid = pwd.getpwnam(user).pw_uid
gid = grp.getgrnam(user).gr_gid

if not output_dir_exists:
    os.mkdir(output_dir, 0o755)
    os.chown(output_dir, uid, gid)
    f = open(output_dir + log_file, "w")
    f.close()

os.chdir(output_dir)

zips = os.listdir(input_dir)
zips.sort()

f = open(log_file, "a")
new_sites = ""
for z in zips:
    if z.endswith(ext):
        site = z[:-4]
        if site in os.listdir(output_dir):
            continue
        os.mkdir(site, 0o755)
        os.chown(site, uid, gid)
        os.chdir(site)
        new_sites += (site + "\n")
        try:
            with ZipFile(input_dir + z) as item:
                try:
                    item.extractall()
                except RuntimeError as e:
                    print(z)
                    print(e)
        except BadZipFile as e:
            print(z)
            print(e)
        os.chdir(output_dir)

f.write(new_sites)
f.close()
print(new_sites)