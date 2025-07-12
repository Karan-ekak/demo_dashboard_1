import requests
import os


def download_video(url, output_file_path):
    """Downloads a video from a URL to a file.

    Args:
        url: The URL of the video to download.
        output_file_path: The path to the file where the video will be saved.
    """
    try:
        print(url)
        new_url=url.replace('dl=0','dl=1')
        print(new_url)
        print(f"Downloading Video : {output_file_path}")
        response = requests.get(new_url, stream=True)
        with open(output_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloading Video End : {output_file_path}")
        return True
    except Exception as Err:
        print(f"Error in Download Video : {Err}")
        return False
