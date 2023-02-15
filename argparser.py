import argparse
from argparse import RawTextHelpFormatter
from os import path

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter,
    prog="System Integrity Verifier (siv)", 
    description="Verifies the integrity of a filesytem",
    add_help=False,
    epilog= 
"""
Example 1: Initialization mode with valid syntax (siv in the current working directory)\n 
\t./siv -i  -D important_directory -V verificationDB -R my_report.txt -H sha1\n
Example 2: Verification mode with valid syntax (siv in the current working directory)\n
\t./siv -v -D important_directory -V verificationDB -R my_report2.txt
"""
)
mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('-i', '--init_mode', action='store_true', help="indicates initialization mode")
mode_group.add_argument('-v', '--verif_mode', action='store_true', help="indicates validation mode")
mode_group.add_argument('-h', '--help', action='help', help="show this help message and exit")

parser.add_argument('-D', type=str, action='store', help='path to the destination file', required=True)
parser.add_argument('-V', type=str, action='store', help='path to the verification file', required=True)
parser.add_argument('-R', type=str, action='store', help='path to the report file', required=True)
parser.add_argument('-H', choices=['sha1','md5'], help='hash function for the verification process')

def valid_paths_in_args(monitored_dir, verif_file_path, report_file_path):
    valid = True
    if not path.exists(monitored_dir):
        print("Error: destination path does not exist")
        valid = False
    if file_is_inside_dir(monitored_dir, verif_file_path):
        print("Error: verification file can't be inside destnation path")
        valid = False
    if file_is_inside_dir(monitored_dir, report_file_path):
        print("Error: report file can't be inside destnation path")
        valid = False
    
    if not valid: parser.print_help()    
    return valid

def file_is_inside_dir(dir_path, file_path):
    return path.abspath(dir_path) in path.abspath(file_path)