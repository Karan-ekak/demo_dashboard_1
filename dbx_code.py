import os
import dropbox
from tqdm import tqdm

import dbx_token # file dbx_token fun define
# import dbx_path as dfa
import datetime  




def is_file_exist(path):
    """_summary_ : CHeck File Exist or Not In Dropbox Folder

    Args:
        path (Str): path of Dropbox Folder eg: folder_name/file_name

    Returns:
        Str: File Exist or File Not Exist
    """
    try:
        dbx=dbx_token.dbx_token()
        dbx.files_get_metadata(path)
        return "File Exist"
    except:
        return "File Not Exist"
    

def dropbox_get_link(dbx,dropbox_file_path):
    """Get a shared link for a Dropbox file path.

    Args:
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Returns:
        link: The shared link.
    """

    try:
        # dbx = dbx_token.dbx_token()
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path)
        shared_link = shared_link_metadata.url
        return shared_link.replace('?dl=0', '?raw=1')
    except dropbox.exceptions.ApiError as exception:
        if exception.error.is_shared_link_already_exists():
            shared_link_metadata = dbx.sharing_get_shared_links(dropbox_file_path)
            shared_link = shared_link_metadata.links[0].url
            return shared_link.replace('?dl=0', '?raw=1')


def upload_file(dbx,dbx_path,computer_path):
    try:
        client = dbx
        print("[SUCCESS] dropbox account linked")
        a=dbx.files_upload(open(computer_path, "rb").read(), dbx_path, mode=dropbox.files.WriteMode.overwrite)
        print("[UPLOADED] {}" .format(computer_path))
        print(a)
        return True
    except Exception as E:
        print('Error Exception as E',E)
        return False

def reading_file(folder_path):
    """
    In Every Iteration Its Return less than 499 files
    example if We have 900 files
        1st Iteration return 499 files
            and 2 Iteration return 401 files
    """
    try:
        dbx = dbx_token.dbx_token()
        result = dbx.files_list_folder(folder_path, recursive=True)
    except Exception as e:
        print(e)
        print("Error in Dbx_Token")
    file_list = []
    try:

        def process_entries(entries):
            # Function for fetching Files in Dropbox
            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    file_list.append(entry.name)


        process_entries(result.entries)

        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            process_entries(result.entries)
    except Exception as e:
        print("Error in Exception ",e)

    return file_list



def upload(
    access_token,
    file_path,
    target_path,
    timeout=900,
    chunk_size=4 * 1024 * 1024,
):
    

    """ Upload Large In Dropbox"""

    
    dbx = dropbox.Dropbox(access_token, timeout=timeout)





    with open(file_path, "rb") as f:
        file_size = os.path.getsize(file_path)
        chunk_size = 4 * 1024 * 1024
        if file_size <= chunk_size:
            print(dbx.files_upload(f.read(), target_path))
        else:
            with tqdm(total=file_size, desc="Uploaded") as pbar:
                upload_session_start_result = dbx.files_upload_session_start(
                    f.read(chunk_size)
                )
                pbar.update(chunk_size)
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=f.tell(),
                )
                commit = dropbox.files.CommitInfo(path=target_path)
                while f.tell() < file_size:
                    if (file_size - f.tell()) <= chunk_size:
                        print(
                            dbx.files_upload_session_finish(
                                f.read(chunk_size), cursor, commit
                            )
                        )
                    else:
                        dbx.files_upload_session_append(
                            f.read(chunk_size),
                            cursor.session_id,
                            cursor.offset,
                        )
                        cursor.offset = f.tell()
                    pbar.update(chunk_size)




# upload(access_token, source_file, dest_file)

if __name__=='__main__':
    print("Start")
    
    file_list=reading_file('/Ganecos/Cam1/')
    print(file_list)