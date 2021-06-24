# blogpostUpdater
<p> A program to reformat obsidian markdown images to work with github </p> 

## Installation
blogpostUpdater utilizes [pipx](https://pipxproject.github.io/pipx/) to handle environment isolation from other tools. Installation for pipx can be found [here](https://pipxproject.github.io/pipx/installation/), then clone the repo and run:

Step 1:
```text
┌──(root💀HOST)-[/opt]
└─# cd blogpostUpdater
```

Step 2: Install blogpostUpdater with pipx
```text
┌──(root💀HOST)-[/opt/blogpostUpdater]
└─# pipx install .
```
<p></p>

## Usage
This program should be used to reformat obsidian markdown images to work with Github README syntax. It should be run in the same folder as the images for the markdown. Obsidian makes this easy by storing everything in a "Vault".
1. It creates a directory for the project where all data will be stored. 
2. Then it utilizes regex to extract the images in the obsidian markdown, copies the image files to a new directory and renames them. 
3. Finally, it replaces the image links in the markdown and writes out to a new file. 

The '-p' project folder can then be uploaded to Github and placed in the root of the repo and all images will display correctly for the markdown document in the project folder.

### Command line
```text
optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Base repository URL
  -f FILE, --file FILE  Markdown file to update
  -p PROJECT, --project PROJECT
                        Project name for all files and directories
  -b BRANCH, --branch BRANCH
                        Branch to use for the links (Default: main)
  -v, --verbose         Branch to use for the links
```
<p></p>

### Example 1
```text
root@system # blogupdater -u "https://github.com/theRealFr13nd/tempBlog" -p "Infrastructure Part 1" -f Blogpost.md
[+] Creating project directory: Infrastructure Part 1
[+] Creating assets directory: Infrastructure Part 1/assets
[+] Copying and renaming image files

[+] Data written to folder: Infrastructure Part 1
```

File structure:
```text
PS C:\> tree
C:.
└───Infrastructure Part 1
    └───assets
```
