import os
from core.config import AppConfig


def get_not_imported_requests():
    dirs = AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY.split("/")
    for dir_count in range(len(dirs)):
        not_imported_file_dir = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{"/".join(dirs[0:dir_count+1])}"
        if not os.path.isdir(not_imported_file_dir):
            return None

    return map(
        lambda x: x.strip().split(".")[0].strip(),
        [
            file
            for file in os.listdir(not_imported_file_dir)
            if os.path.isfile(os.path.join(not_imported_file_dir, file))
            and file.endswith("__google_map.xlsx")
        ],
    )


def get_imported_requests():
    dirs = AppConfig.IMPORTED_SHEETS_DIRECTORY.split("/")
    for dir_count in range(len(dirs)):
        imported_file_dir = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{"/".join(dirs[0:dir_count+1])}"
        if not os.path.isdir(imported_file_dir):
            return None

    return map(
        lambda x: x.strip().split(".")[0].strip(),
        [
            file
            for file in os.listdir(imported_file_dir)
            if os.path.isfile(os.path.join(imported_file_dir, file))
            and file.endswith("__google_map.xlsx")
        ],
    )
