import subprocess
import os

camera_id = 'cam3'
BASE_DIR = '/home/EKAK/kanplas-2/cam3_cutting_china7/'
uploaded_video_path = f'{BASE_DIR}/{camera_id}_videos/'
render_video_path = f'{uploaded_video_path}render_videos/'
STATIC_FOLDER_PATH = "/home/EKAK/Kanplas-dashboard-dev/static/render_videos/"

def check_video_in_static(incident_id):
    files = os.listdir(STATIC_FOLDER_PATH)
    # print(files)
    for file in files:
        try:
            converted_video_id = int(((file.split('_'))[-1].split('.'))[0])
            if incident_id == converted_video_id:
                return file
        except ValueError:
            continue
    return False

def fix_corrupted_video(input_video, output_video):
    """Try to fix a corrupted MP4 file using FFmpeg."""
    try:
        command = [
            "ffmpeg",
            "-err_detect", "ignore_err",
            "-i", input_video,
            "-c", "copy",
            "-movflags", "+faststart",
            output_video
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to fix corrupted video: {input_video}")
        return False

def compare_video_id(incident_id):
    print("🔄 Checking videos for conversion:", incident_id)

    files = os.listdir(render_video_path)

    for file in files:
        try:
            render_video_id = int(((file.split('_'))[-1].split('.'))[0])
            if incident_id == render_video_id:
                print("🎬 Processing video:", file)
                input_video = f'{render_video_path}{file}'
                output_video = f"{STATIC_FOLDER_PATH}{file}"

                # Check if the video is corrupted
                check_command = ["ffmpeg", "-v", "error", "-i", input_video, "-f", "null", "-"]
                check_result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if "moov atom not found" in check_result.stderr.decode():
                    print("⚠️ Video is corrupted. Attempting to fix...")
                    if not fix_corrupted_video(input_video, output_video):
                        print("❌ Could not fix the video. Skipping...")
                        return False

                # Convert the video
                command = [
                    "ffmpeg",
                    "-i", input_video,
                    "-c:v", "libx264",
                    "-crf", "23",
                    "-preset", "fast",
                    "-an",  # Disables audio
                    output_video
                ]

                subprocess.run(command, check=True)
                # print("✅ Video converted successfully:", file)
                return file
        except (ValueError, subprocess.CalledProcessError) as e:
            print(f"❌ Error processing {file}: {e}")
            continue

    print("⚠️ No matching video found.")
    return False







BASE_DIR2 = '/home/EKAK/kanplas-2/cam3_defect_cutting_china7/'
uploaded_video_path2 = f'{BASE_DIR2}/{camera_id}_videos/'
render_video_path2 = f'{uploaded_video_path2}render_videos/'
STATIC_FOLDER_PATH2 = "/home/EKAK/Kanplas-dashboard-dev/static/render_videos/"



def check_video_in_static2(incident_id):
    files = os.listdir(STATIC_FOLDER_PATH2)
    print("FILES OF DEFECTS :",files)
    for file in files:
        try:
            converted_video_id = int(((file.split('_'))[-1].split('.'))[0])
            if incident_id == converted_video_id:
                print("if incident_id == converted_video_id: for defects:",converted_video_id)
                return file
        except ValueError:
            continue
    return False

def fix_corrupted_video2(input_video, output_video):
    """Try to fix a corrupted MP4 file using FFmpeg."""
    try:
        command = [
            "ffmpeg",
            "-err_detect", "ignore_err",
            "-i", input_video,
            "-c", "copy",
            "-movflags", "+faststart",
            output_video
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to fix corrupted video: {input_video}")
        return False

def compare_video_id2(incident_id):
    print("🔄 Checking videos for conversion:", incident_id)

    files = os.listdir(render_video_path2)

    for file in files:
        try:
            render_video_id = int(((file.split('_'))[-1].split('.'))[0])
            if incident_id == render_video_id:
                # print("🎬 Processing video:", file)
                input_video = f'{render_video_path2}{file}'
                output_video = f"{STATIC_FOLDER_PATH2}{file}"

                # Check if the video is corrupted
                check_command = ["ffmpeg", "-v", "error", "-i", input_video, "-f", "null", "-"]
                check_result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if "moov atom not found" in check_result.stderr.decode():
                    print("⚠️ Video is corrupted. Attempting to fix...")
                    if not fix_corrupted_video(input_video, output_video):
                        print("❌ Could not fix the video. Skipping...")
                        return False

                # Convert the video
                command = [
                    "ffmpeg",
                    "-i", input_video,
                    "-c:v", "libx264",
                    "-crf", "23",
                    "-preset", "fast",
                    "-an",  # Disables audio
                    output_video
                ]

                subprocess.run(command, check=True)
                # print("✅ Video converted successfully:", file)
                return file
        except (ValueError, subprocess.CalledProcessError) as e:
            print(f"❌ Error processing {file}: {e}")
            continue

    print("⚠️ No matching video found.")
    return False
