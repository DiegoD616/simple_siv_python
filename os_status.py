from stat import S_ISDIR, S_ISREG
from os import path, stat
import hashlib
from pathlib import Path

def get_status_dict(pathname, hash_type, dir_hash):
    os_file_stat = stat(pathname)
    os_status = {
        'mode':os_file_stat.st_mode, 'uid':find_owner(pathname, os_file_stat),
        'gid':find_group(pathname, os_file_stat), 'size':os_file_stat.st_size, 
        'mtime':os_file_stat.st_mtime_ns
    }
    
    if S_ISDIR(os_status['mode']):
        hex_to_save = dir_hash.hexdigest()
    elif S_ISREG(os_status['mode']):
        hash = hashlib.new(hash_type)
        with open(pathname,'rb') as file_to_hash: 
            hash.update(file_to_hash.read())
            file_to_hash.seek(0)
            if dir_hash is not None: 
                dir_hash.update(file_to_hash.read())
        hex_to_save = hash.hexdigest()
    
    os_status["hash"] = hex_to_save
    os_status["path"] = path.abspath(pathname)
    return os_status

def find_owner(path, file_stat):
    try:
        path = Path(path)
        return f"{path.owner()}"
    except Exception:
        return file_stat.st_uid

def find_group(path, file_stat):
    try:
        path = Path(path)
        return f"{path.group()}"
    except Exception:
        return file_stat.st_gid