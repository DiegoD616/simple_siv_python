# **System Integrity Verifier (SIV)**

Diego Díaz Fonseca ([diazfonseca.diego@gmail.com](diazfonseca.diego@gmail.com))

## 1 Introduction
This repo contains the implementation for a system integrity verifier made with python 3.9. A System Integrity Verifier, or SVI for short, is a program that is designed to detect any errors or discrepancies in a computer system. It can detect any issues with the code, hardware, or data that may be present in the system. The System Integrity Verifier can also compare the results of the program to predetermined criteria in order to ensure that the program is functioning as expected. In addition, the System Integrity Verifier can monitor the system for any potential security risks or vulnerabilities. By using a System Integrity Verifier, organizations can ensure that their computer systems are functioning properly and are secure from potential threats.

Knowing what an SVI is lets now talk about this implementation and design choices that were made. This implementation has a initialization and verification mode. What this modes are and how the work is shown in the next section. Section 3 has examples of it can be used.

## 2 Design and implementation
An SVI detects changes in a tree structure of files. In order to detect these changes with need to find a way to represent and save the current state of the tree into a file which will call verificationDB, this file will include all the information we need to detect the changes made. This verificationDB has the format of a comma separated value. The first line specifies the hash method use during the creation, the second line specifies the columns which are the following:
1. path: This is a string with the absolute path to the file or directory being saved. This column works as an id, to identify each file o directory uniquely.
1. size: This integer represents the size of the file or directory.
1. uid: This string represents the username of the user who owns the files in the filesystem.
1. gid: This string represents the group name of the user who owns the files in the filesystem.
1. mode: this integer represents the permissions to access the file, represented with standard way unix represent permissions.
1. mtime: this is an integer which show the amounts of nanoseconds since epoch. It is used represent the last time the contents of the file were modified.
1. hash: this integer is a number that represents uniquely the contents of a file.
From the third row onward each line are entries for files found in the file system. The values are added to the row in the same order as listed before. 

The creation of the verificationDB requires an algorithm to descend the tree structure recursively, the algorithm obtains the file’s metadata every time it detects a file or directory. This is done using python’s stat module from the os library. At this point the hash of the content is created, for files its content is hashed for directories the creation of the hash takes into account the contents of all its contained files. This hashes are produced with pythons hashlib library.

The tree descending algorithm takes a callback function, which is called for every file or directory found during the descending. For the initialization the callback is use to collect the required info and wirte it to the verificationDB.

Essentially, running the initialization mode is the creation of the verificationDB file. This file is then used in the verification mode.

The verification mode consist of reading the verificationDB, which means to read the old state of the tree, and compare to the current state. The verification mode uses a different callback  function. This callback function gets the current state of the metadata of the current file being analyze and compares it with saved data. Every time an inconsistency is found a warning is raised. First it searches the verificationDB for an entry identified with its path, if this entry can’t be found than the file is new raising a warning. If the entry was found then the information saved in that entry is compared to the current metadata, every variable listed at the beginning of this section is compared to find changes. Every time a variable has a change a warning is raised. For a warning to be raised means a line explaining the inconsistency will be written in the report file.

## 3 Usage
This SIV can be used from the a BASH terminal where python is install. The testing was done in python 3.9.16. In addition, the computer where this runs must have installed the following packages: 
* certifi==2022.12.7
* numpy==1.24.2
* pandas==1.5.3
* python-dateutil==2.8.2
* pytz==2022.7.1
* six==1.16.0
All the packages listed above can be install with the package manager pip, also it is recommended to create a python virtual environment where to install the specified versions of the packages. 
The command line interface for this program follows this format:
```
python main.py (-i | -v | -h) -D D -V V -R R [-H {sha1,md5}]
```
where the arguments arguments work like such:
* -i, --init_mode   indicates initialization mode
* -v, --verif_mode  indicates validation mode
* -h, --help        show this help message and exit
* -D D              path to the destination file
* -V V              path to the verification file
* -R R              path to the report file
* -H {sha1,md5}     hash function for the verification process

Examples 1: Initialization mode with valid syntax (siv.py in the current working directory)
```
python siv.py -i  -D ~/Documents/ -V verificationDB.csv -R my_report.txt -H sha1
python siv.py -i  -D ~/Accounting_files/ -V verificationDB -R my_report.txt -H md5
```

Example 2: Verification mode with valid syntax (siv.py in the current working directory)
```
python siv.py -v -D ~/Documents -V verificationDB -R my_report2.txt
```
