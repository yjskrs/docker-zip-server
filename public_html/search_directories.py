"""
Lists webpage-like files in directories.

Returns list (all directories) of lists (all subdirectories/files)
"""
import os
import sys

PHP_EXT = ".php"
HTML_EXT = ".html"
HTM_EXT = ".htm"

def search_directories(kits):
    """Iterates through all directories to find webpage-like files
    Parameters
    ----------
    kits : array
        The directories to iterate through

    Return
    ------
    results : 2D array
    """
    results = []
    for i in kits:
        results.append([])
        results[-1] = list(dict.fromkeys(search_one_directory(i)))
        if (len(results) == 0):
            results.pop()
    results.sort(key=len)         
    print("================ Complete search! ================")
    return results


def search_one_directory(path):
    """Traverses through given directory to find webpage-like files.
    Parameters
    ----------
    path : string
        The path of the directory to traverse through
    
    Return
    ------
    found : 1D array
        Array of relevant file paths
    """
    # files = os.listdir(path)
    found = recurse_directory(path, path)
    found = heuristics_filter(found)
    return found

def recurse_directory(base, curr):
    found = []
    if os.path.isdir(curr):
        try:
            files = os.listdir(curr)
            files.sort(key=sort_dir_lambda)
            for i in files:
                found = found + recurse_directory(base, curr + "/" + i)
        except Exception as e:
            print("ERROR: Unable to traverse directory " + curr)
            print(e)
    else:
        if isWebpage(curr):
            found.append(curr)
    return found

def sort_dir_lambda(x):
    if x.endswith("/index.html") or x.endswith("/index.php"):
        return 0
    elif x.endswith(".html") or x.endswith(".htm"):
        return 1
    elif x.endswith(".php"):
        return 2
    else:
        return 3

def heuristics_filter(files):
    """Check whether there are more than a certain number of heuristic files.
    """
    heuristics = ["index.html", "index1.html", "index2.html",
                  "index.php", "index1.php", "index2.php",
                  "login.html", "login1.html", "login.php", "login1.php"]
    if len(files) >= 80:
        filtered = []
        for x in files:
            for h in heuristics:
                if h in x:
                    filtered.append(x)
        if (len(filtered) >= 20):
            return filtered
        else:
            files.sort(key=sort_dir_lambda)
            for x in files:
                if x not in filtered:
                    filtered.append(x)
                if (len(filtered) >= 3000):
                    break
            return filtered
    return files

def isWebpage(filename):
    return filename.endswith(PHP_EXT) \
        or filename.endswith(HTML_EXT) \
            or filename.endswith(HTM_EXT)

def log_openable_files(logdir, logfile, results):
    """Logs the openable files in a log file.
    Parameters
    ----------
    logdir : str
        The directory to save the logfile
    logfile : str
        The logfile to save the results
    results : 2D array
        The results of directory listing, where the outer array represents
        the highest level directory and the inner array represents each webpage-like
        file found in the directory
    """
    # results is a 2d array
    os.chdir(logdir)
    try:
        with open(logfile, 'w') as f:
            for i in results:
                if len(i):
                    for j in i:
                        f.write(j + "\n")
                    f.write("\n")
    except Exception as e:
        print("ERROR: Unable to write log")
        print(e)

    return

if __name__ == "__main__":
    args = sys.argv[1:] # python3 search_directories.py BASE_DIR
    BASE_DIR = './'
    LOG_DIR = '/var/www/logs/'
    LOG_FILE = 'log.txt'
    
    kits = kits = [ BASE_DIR + i for i in os.listdir(BASE_DIR) ]
    kits.sort()

    all_files = search_directories(kits)

    log_openable_files(LOG_DIR, LOG_FILE, all_files)
