import dropbox
import dbx_token
# import dbx_path as dfa
from os import walk
import os
from pathlib import Path
from pprint import pprint
import sys

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

def is_file_exist(path):
    try:
        dbx=dbx_token.dbx_token()
        a=dbx.files_get_metadata(path)
        print(a)
        return "File Exist"
    except:
        return "File Not Exist"

def generate_shared_link(path):
    try:
        dbx=dbx_token.dbx_token()
        link=dbx.sharing_create_shared_link('/Argus_Device/Argus_104/attendanceImages/Dakash__2023_07_19__08_13.jpg').url
        print(link)
        return link.replace('dl=0', 'raw=1')
        # return "File Exist"
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
        print(1)
        dbx = dbx_token.dbx_token()
        print(2)
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path)
        print("\n\n\nGet Shared Link",shared_link_metadata)
        print(3)
        shared_link = shared_link_metadata.url
        print(4)
        return shared_link.replace('?dl=0', '?raw=1')
    except dropbox.exceptions.ApiError as exception:
        print("Its Exception", exception)
        print(str(exception))
        print("\n\n\n Error ",exception.error.is_shared_link_already_exists)
        if exception.error.is_shared_link_already_exists():
            shared_link_metadata = dbx.sharing_get_shared_links(dropbox_file_path)
            print("\n\n\nGet Shared Link",shared_link_metadata)
            shared_link = shared_link_metadata.links[0].url
            return shared_link.replace('?dl=0', '?raw=1')
   
    
def reading_file(folder_path:str):
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

def download_each(computer_path,dbx_path):
    try:
        dbx=dbx_token.dbx_token()
        with open(computer_path, "wb") as f:
            metadata, res = dbx.files_download(path=dbx_path)
         
            f.write(res.content)
            
    
            f.close()
        return True
    except Exception as e:
        print(e)
        return False
# folder_path = dfa.dbx_video('Dave_101')
# a= reading_file(folder_path)
# print(a)
# print(len(a))


def upload_large_file(computer_path, dbx_file_path, shouldDelete, overwrite):
    dbx=dbx_token.dbx_token()
    LOCALFILE = file = computer_path
    BACKUPPATH = dbx_file_path
    if 'current' in computer_path.split('/')[-1]:
        return
    print('LOCALFILE = ' + LOCALFILE)
    print('BACKUPPATH = ' + BACKUPPATH)
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        #logger1.info('upload  {} finished'.format(str(LOCALFILE + " as " + BACKUPPATH)))
        try:
            file_size = os.path.getsize(LOCALFILE)

            CHUNK_SIZE = 4 * 1024 * 1024

            if file_size <= CHUNK_SIZE:
                print('small file size, directly uploading')
                #logger1.info('size =  {}, uploading directly'.format(file_size))
                if overwrite == 1:
                    print(dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))) # this also has an overwrite element, which can be a flag
                else:
                    print(dbx.files_upload(f.read(), BACKUPPATH))
                    #print(dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))) # this also has an overwrite element, which can be a flag

            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path=BACKUPPATH)

                while f.tell() < file_size:
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE),
                                                        cursor,
                                                        commit))
                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE),
                                                        cursor.session_id,
                                                        cursor.offset)
                        cursor.offset = f.tell()
            #DELETE FILE
            if shouldDelete == 1:
                os.remove(LOCALFILE)

        except ApiError as err:
            # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
                #logger1.info('ERROR: Cannot back up; insufficient space.')
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

if __name__=='__main__':
    import csv
    # dbx= dbx_token.dbx_token()
    # files=dbx.files_list_folder('/ganecos/Cam1')
    # print(files)
    file_path = "ganecos_Cam_video.txt"  # Replace with your desired file path

    all_file_list= reading_file('/ganecos/cam1')
    print(all_file_list)
    # with open('dbx_all_files.csv','w') as file:
    #     writer=csv.writer(file)
    #     writer.writerows(all_file_list)

    try:
        with open(file_path, "w") as file:
            # Write content to the file
            file.write(F"{all_file_list}")
            # file.write("This is the second line of text.\n")
    except IOError as e:
        print(f"Error writing to file: {e}")
    # all_file_list= reading_file('/')
    # print(all_file_list)
    # with open('dbx_all_files.csv','w') as file:
    #     writer=csv.writer(file)
    #     writer.writerows(all_file_list)