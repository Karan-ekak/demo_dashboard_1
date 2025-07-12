"""
Step 0 : Get the New Video List
Step 1 : Download Video from Dropbox 
Step 2 : Applied Algorithm and 
Step 3 : Save Incident Values into DB

"""

import dropbox
import os
from loguru import logger

# Local Modules
from database_connection import ArgusDB
import dbx_code2 as dbx_code
import cam1_algo
import dbx_token
# Logging File Creation
logger.add('logs/Ganecos.log',level="INFO",rotation='100 MB')

# Constants
device_id=['Argus_105','Argus_201']

# Path 
dbx_video_path='/Ganecos/Cam1'
basedir=0


def main():
    basedir=os.path.abspath(os.path.dirname(__file__))
    device_video_path=basedir+'/Argus_105/videos/'
    
    # Step 1 : | Start | Get the New Video List
    video_list=dbx_code.reading_file(folder_path=dbx_video_path)
    # print(video_list)
    # Step 1 : | End |
    
    if not video_list:
        # No Video Found
        print("No Video Found")
        return False
    
    # downloaded_video=download_video_dbx(video_list)
    # dbx=dbx_token.dbx_token()
    print(video_list)
    for each_video in video_list :
        print(f"Video File Name : {each_video}")
        try:
            # file_name=each_video
            video_path=device_video_path+each_video
            # if each_video[0] == ' ':
            #     # First Character Check then Remove
            #     dbx.files_move(dbx_video_path+'/'+each_video, dbx_video_path+'/'+each_video[1:])
            #     print('Renaming ',each_video)
            
            #     # Repace New Space in New Name
            #     if ' ' in each_video:
            #         file_name= each_video.replace(' ','_')
            #         dbx.files_move(dbx_video_path+'/'+each_video[1:], dbx_video_path+'/'+file_name)
            #         print("Removing Space")
            
            # # Only Replace Space
            # if ' ' in file_name:
            #     file_name= each_video.replace(' ','_')
            #     dbx.files_move(dbx_video_path+'/'+each_video, dbx_video_path+'/'+file_name)
            #     print("Removing Space")
                
            # Step 2 : | Start | Download The Each Video
            logger.info(f'Starting Downloading Video : {each_video}')
            
            status_video_download=dbx_code.download_each(device_video_path+each_video,dbx_video_path+'/'+each_video)
        except Exception as E:
            print(E)
            print("Issue in Download")
        
        # #Step 3 : | Start |  Apply Algo 
        if status_video_download:
            # Apply Algo
        
            logger.info(f'_Downloaded Video : {each_video}')
            logger.info('_Algo Executing python3 /home/paperspace/argus/argus-backend-1/app_notification3.py {video_path} &')
            os.system(f'python3 /home/paperspace/ganecos/cam1_algo.py {video_path} &')

        
        
       
        # Step 4 | Start | Uploaded Incident into DB
        print('DB Operation')
        
        # Step 4 | End | Uploaded Incident into DB
        
    #Step 3 : | End |  Apply Algo
    
    
    return True
    # pass


if __name__ == '__main__':
    main()






