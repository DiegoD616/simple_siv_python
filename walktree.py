from os import stat, path
from stat import *
import os
import hashlib

def walktree(top, callback, callback_params, father_hash=None):
    '''recursively descend the directory tree rooted at top, calling the callback'''
    total_dirs_parsed, total_files_parsed, total_callback_counter = 0, 0, 0
    for f in os.listdir(top):
        pathname = path.join(top, f)
        mode = os.lstat(pathname).st_mode
        if S_ISDIR(mode):
            current_dir_hash = hashlib.new(callback_params["hash_type"])
            parsed_dirs, parsed_files, callback_counter = walktree(pathname, callback, callback_params, current_dir_hash) # It's a directory, recurse into it
            callback_counter = callback(pathname, current_dir_hash, **callback_params)
            total_dirs_parsed += 1 + parsed_dirs
            total_files_parsed += parsed_files
            total_callback_counter += callback_counter
        elif S_ISREG(mode):
            callback_counter = callback(pathname, father_hash, **callback_params)
            total_files_parsed += 1
            total_callback_counter += callback_counter

    return total_dirs_parsed, total_files_parsed, total_callback_counter