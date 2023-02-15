from datetime import datetime
from walktree import walktree
from os_status import get_status_dict

def init_mode(monitored_dir, verif_file_path, report_file_path, hash_function):
    with open(verif_file_path, 'w') as verif_file, open(report_file_path, 'w') as report_file:
        callback_params = {'verif_file':verif_file, 'hash_type':hash_function}
        verif_file.write(f"{hash_function}\npath,size,uid,gid,mode,mtime,hash\n")
        total_dirs_parsed, total_files_parsed, _ = walktree(monitored_dir, write_to_verif_file, callback_params)
        write_init_report(report_file, verif_file_path, report_file_path, total_dirs_parsed, total_files_parsed)

def write_to_verif_file(pathname, dir_hash, verif_file, hash_type):
    os_status_dict = get_status_dict(pathname, hash_type, dir_hash)
    verif_file.write(
        f'"{os_status_dict["path"]}",{os_status_dict["size"]},"{os_status_dict["uid"]}",'+
        f'"{os_status_dict["gid"]}",{os_status_dict["mode"]},{os_status_dict["mtime"]},{os_status_dict["hash"]}\n'
    )
    return 0

def write_init_report(report_file, verif_file_path, report_file_path, total_dirs_parsed, total_files_parsed):
    report_file.write("{\n")
    report_file.write(f"\tverification_file_path:\"{verif_file_path}\"\n")
    report_file.write(f"\treport_file_path:\"{report_file_path}\"\n")
    report_file.write(f"\ttotal_directries_parsed:\"{total_dirs_parsed}\"\n")
    report_file.write(f"\ttotal_files_parsed:\"{total_files_parsed}\"\n")
    report_file.write(f"\ttime_completed_init_initialization:\"{datetime.now()}\"\n")
    report_file.write("}")