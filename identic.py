# This program will traverse the directories and look for files or directories that are duplicates of each other (i.e. identical)

import argparse
import os
import subprocess
import hashlib
from collections import defaultdict

workingDirectory = subprocess.check_output('pwd', shell=True)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-d', action="store_true", default=False)  # identical directories
group.add_argument('-f', action="store_true", default=False)  # identical files
parser.add_argument("-c", action="store_true", default=False)  # Identical means the contents are exactly the same
parser.add_argument("-n", action="store_true", default=False)  # Identical means the names are exactly the same
parser.add_argument("-s", action="store_true", default=False)  # The size for each duplicate will also be printed
parser.add_argument("dirList", nargs='*', type=str, action="store", default=[(workingDirectory.decode())[:-1]])

# default arguments
args = parser.parse_args()
if not args.d and not args.f:
    args.f = True
if not args.c and not args.n:
    args.c = True

everything = defaultdict(list)  # hash values: corresponding file or directory paths
knownSubDirectoryHashes = dict()  # pre-calculated directory paths: corresponding hashes

if args.f:
    while args.dirList:
        fullPathName = os.path.abspath(args.dirList.pop())  # handle relative path condition
        ls = os.listdir(fullPathName)
        for current in ls:
            currentFullName = os.path.join(fullPathName, current)
            if os.path.isdir(currentFullName):  # append current directory to dirList to traverse in the future
                args.dirList.append(currentFullName)
            elif os.path.isfile(currentFullName):  # calculates the file's hash
                currentHash = ""
                if args.n and not args.c:  # if n option is used, take the hash of the name
                    n = hashlib.sha256(current.encode())
                    currentHash = n.hexdigest()
                elif args.c and not args.n:  # if c option is used, read in byte format, take the hash of the content
                    with open(currentFullName, "rb") as f:
                        content = f.read()
                        currentHash = hashlib.sha256(content).hexdigest()
                else:  # if cn option is used, takes both name's and content's hash and concatenate
                    names_hash = hashlib.sha256(current.encode()).hexdigest()
                    with open(currentFullName, "rb") as f: # read in byte format and takes the hash of the content
                        content = f.read()
                        contents_hash = hashlib.sha256(content).hexdigest()
                        currentHash = hashlib.sha256((names_hash + contents_hash).encode()).hexdigest()

                if (currentHash not in everything) or (currentFullName not in everything.get(currentHash)):
                    everything[currentHash].append(currentFullName)

if args.d:
    for dirArgument in args.dirList:
        walker = list(os.walk(dirArgument, topdown=False))
        for root, subdirectories, fileNames in walker:
            hashlist = list()  # hash values of subdirectories and files

            for filename in fileNames:
                fullFileName = os.path.join(root, filename)
                if args.n and not args.c:  # if n option is used, take the hash of the file name
                    hashlist.append(hashlib.sha256(filename.encode()).digest().hex())
                elif args.c and not args.n:
                    with open(fullFileName, 'rb') as f: # if c option is used, read in byte format, take the hash of the content
                        content = f.read()
                        hashlist.append(hashlib.sha256(content).digest().hex())
                else: # if cn option is used, take both name's and content's hash and concatenate
                    names_hash = hashlib.sha256(filename.encode()).digest().hex()
                    with open(fullFileName, 'rb') as f:  # read in byte format and takes the hash of the content
                        content = f.read()
                        contents_hash = hashlib.sha256(content).digest().hex()
                        hashlist.append((hashlib.sha256((names_hash + contents_hash).encode()).hexdigest()))

            for subdir in subdirectories:
                names_hash = hashlib.sha256(subdir.encode()).digest().hex()
                fullSubDirName = os.path.join(root, subdir)
                subHash = knownSubDirectoryHashes[fullSubDirName]  # look up for the hash value of the subdirectory
                subHashHash = hashlib.sha256(subHash).digest().hex()
                if args.n:
                    hashlist.append((hashlib.sha256((names_hash + subHashHash).encode()).hexdigest()))
                else:
                    hashlist.append(subHashHash)

            if args.n:
                hashlist.append(hashlib.sha256((os.path.basename(root)).encode()).digest().hex())

            hashlist.sort()
            currentHash = hashlib.sha256()
            for i in hashlist:
                currentHash.update(i.encode())
            currentHash = currentHash.digest()
            if (currentHash not in everything) or (root not in everything.get(currentHash)):
                everything[currentHash].append(root)
            knownSubDirectoryHashes[root] = currentHash

duplicates = list()
duplicatesSize = list()


# recursively calculate the size of a directory
def directorySize(dir):
    totalSize = os.path.getsize(dir)
    for item in os.listdir(dir):
        fullpath = os.path.join(dir, item)
        if os.path.isdir(fullpath):
            totalSize += directorySize(fullpath)
        elif os.path.isfile(fullpath):
            totalSize += os.path.getsize(fullpath)
    return totalSize


for i in everything:
    if len(everything[i]) > 1:
        everything[i].sort()
        duplicates.append(everything[i])
        sizeList = list()
        if args.s and args.c:
            for dupp in sorted(everything[i]):
                if args.f:
                    size = os.path.getsize(dupp)
                else:
                    size = directorySize(dupp)
                sizeList.append((size*(-1), dupp))
            sizeList.sort()
            duplicatesSize.append(sizeList)

# every duplicate set is sorted alphabetically in itself
# print full path names of duplicates
if args.s and args.c:
    duplicatesSize.sort()
    for i in duplicatesSize:
        for dupsizepair in i:
            print(dupsizepair[1], '\t', dupsizepair[0]*(-1))
        print('\n')

else:
    duplicates.sort()
    for i in duplicates:
        i.sort()
        for x in range(len(i)):  # print duplicate group
            print(i[x])
        print('\n')
