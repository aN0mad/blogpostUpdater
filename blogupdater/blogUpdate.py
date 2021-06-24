import argparse
import os
import re
import shutil
import sys

# Strip markdown formatting from image name
def cleanup(item):
    item = item.strip("!").strip("[[").strip("]]")
    return item

# Command line arg parsing
def doArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Base repository URL")
    parser.add_argument("-f", "--file", help="Markdown file to update")
    parser.add_argument("-p", "--project", help="Project name for all files and directories")
    parser.add_argument("-b", "--branch", help="Branch to use for the links (Default: main)")
    parser.add_argument("-v", "--verbose", help="Branch to use for the links ", action="store_true")

    # Parse and manage arguments
    args = parser.parse_args()

    # Arg URL
    if args.url == None:
        parser.print_help()
        print("")
        print("[!] ERROR: -u, --url was not specified")
        sys.exit(1)
    else:
        URL_HEAD = args.url

    # Arg INFILE
    if args.file == None:
        parser.print_help()
        print("")
        print("[!] ERROR: -f, --file was not specified")
        sys.exit(1)
    else:
        if os.path.exists(args.file):
            INFILE = str(args.file)
        else:
            parser.print_help()
            print("")
            print("[!] ERROR: The file "+str(args.file)+" does not exist")
            sys.exit(1)	

    # Arg Project
    if args.project == None:
        parser.print_help()
        print("")
        print("[!] ERROR: -p, --project was not specified")
        sys.exit(1)
    else:
        PNAME = args.project
    
    # Arg Branch
    if args.branch == None:
        BRANCH = "main"
    else:
        BRANCH = args.branch

    return URL_HEAD, INFILE, PNAME, BRANCH, args.verbose

def main():
    # Const
    ASSETS_DIR_NAME = "assets"
    URL_STUB = "/blob/{BRANCH}/{PNAME}/{ASSETS_DIR_NAME}/{FILENAME}"

    # Do argparse
    URL_HEAD, INFILE, PNAME, BRANCH, VERBOSE = doArgs()

    # Other args and vars
    file_, ext = os.path.splitext(INFILE)
    newBlogFile = INFILE # Don't need to change the name because we put it in a different folder
    newOldFiles = {}
    extList = []

    # Open file and find all image names
    with open(INFILE, "r") as blogpostHandle:
        finds = re.findall("\!\[\[.*\]\]", blogpostHandle.read())

    # Create directory for blogpost
    try:
        print("[+] Creating project directory: {0}".format(PNAME))
        os.mkdir(PNAME)
    except:
        pass

    # Create dictionary and map current file names to numbered file names
    looper = 0
    for item in finds:
        newName = cleanup(item)
        if newName not in newOldFiles.keys():
            name, ext = os.path.splitext(newName)
            if ext not in extList:
                extList.append(ext)
            newOldFiles[newName] = PNAME.replace(" ", "_")+"-"+str(looper)+ext
            looper = looper + 1
        else:
            print("[#] Duplicate key found: {0}".format(newName))
            pass

    # Get all files in directory looping over found extensions
    files = []
    for ext in extList:
        files = files + [_ for _ in os.listdir() if _.endswith(ext)]

    # Create asset directory
    ASSETS_DIR = os.path.join(PNAME, ASSETS_DIR_NAME)
    try:
        print("[+] Creating assets directory: {0}".format(ASSETS_DIR))
        os.makedirs(ASSETS_DIR)
    except:
        pass

    # Loop over all image files, rename and move them
    print("[+] Copying and renaming image files")
    for item in newOldFiles.keys():
        if item in files:
            if VERBOSE: print("\t [#] Renaming {0} to {1}".format(item, newOldFiles[item]))
            
            shutil.copy(item, os.path.join(ASSETS_DIR, newOldFiles[item]))
            #os.rename(os.path.join(ASSETS_DIR, item), os.path.join(ASSETS_DIR, newOldFiles[item]))
            files.remove(item)
        else:
            if VERBOSE: print("\t [!] '{0}' not found!".format(item))

    # Read in blogpost data
    oldBlogFileHandle = open(INFILE, "r")
    data = oldBlogFileHandle.read()
    oldBlogFileHandle.close()

    # Find and replace all image links
    for fileName in newOldFiles.keys():
        link = (URL_HEAD+URL_STUB.format(BRANCH=BRANCH, PNAME=PNAME, ASSETS_DIR_NAME=ASSETS_DIR_NAME, FILENAME=newOldFiles[fileName])).replace(" ", "%20")
        fmtImage = "\!\[\[{0}\]\]".format(fileName)
        data = re.sub(fmtImage, "![]({0})".format(link), data)


    # Write new data out to the file
    newBlogFileHandle = open(os.path.join(PNAME, newBlogFile), "w")
    newBlogFileHandle.write(data)
    newBlogFileHandle.close()

    print()
    print("[+] Data written to folder: {0}".format(PNAME))

if __name__ == "__main__":
    main()