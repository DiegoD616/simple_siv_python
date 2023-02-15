from datetime import datetime
from walktree import walktree
from os_status import get_status_dict
from os import path
import pandas

def verification_mode(monitored_path, verif_file_path, report_file_path):
    with open(verif_file_path, 'r') as verif_file, open(report_file_path, 'w') as report_file:
        hash_type = verif_file.readline().strip()
        callback_params = {'verif_data': pandas.read_csv(verif_file), 'hash_type':hash_type, 'report_file':report_file}
        total_dirs_parsed, total_files_parsed, total_warnings = walktree(monitored_path, validate_integrity, callback_params)
        write_validation_report(report_file, monitored_path, verif_file_path, report_file_path, total_dirs_parsed, total_files_parsed, total_warnings)

def validate_integrity(pathname, dir_hash, verif_data, hash_type, report_file):
    warnings_found = 0
    is_new = check_if_new(pathname, verif_data, report_file)
    if is_new == True: warnings_found += 1
    if not is_new:
        file_status = get_status_dict(pathname, hash_type, dir_hash)
        file_verif_data = verif_data[verif_data["path"]==path.abspath(pathname)]
        warnings_found += check_different_attrs(file_status, file_verif_data, report_file)

    return warnings_found

def check_if_new(pathname, verif_data, report_file):
    is_new = not path.abspath(pathname) in verif_data["path"].values

    if is_new:
        report_file.write(f"{pathname} is a new file in the file system")
    
    return is_new

def check_different_attrs(file_attr, file_verif_data, report_file):
    warnings_found = 0
    for attr in file_verif_data:
        old_value = file_verif_data[attr].iloc[0]
        current_value = file_attr[attr]
        if old_value != current_value:
            report_file.write(
            f"""{file_attr["path"]} has changed {attr}. Old. {old_value} Current: {current_value}\n"""
            )
            warnings_found += 1

    return warnings_found

def write_validation_report(report_file, monitored_path, verif_file_path, report_file_path, total_dirs_parsed, total_files_parsed, total_warnings):
    report_file.write("{\n")
    report_file.write(f"\tverification_file_path:\"{monitored_path}\"\n")
    report_file.write(f"\tverification_file_path:\"{verif_file_path}\"\n")
    report_file.write(f"\treport_file_path:\"{report_file_path}\"\n")
    report_file.write(f"\ttotal_directries_parsed:\"{total_dirs_parsed}\"\n")
    report_file.write(f"\ttotal_files_parsed:\"{total_files_parsed}\"\n")
    report_file.write(f"\ttotal_warnings_issued:\"{total_warnings}\"\n")
    report_file.write(f"\ttime_completed_init_initialization:\"{datetime.now()}\"\n")
    report_file.write("}")