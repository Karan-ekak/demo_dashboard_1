
import os
import subprocess
def parse_idle_time_to_minutes(idle_time):

    #Converting H:M format into Minutes only
    total_minutes = 0
    parts = idle_time.lower().split()

    for i in range(len(parts)):
        if parts[i].startswith('hour'):
            total_minutes += int(parts[i - 1]) * 60
        elif parts[i].startswith('min'):
            total_minutes += int(parts[i - 1])

    return total_minutes
idle_time = '2025_02_12_17_36_294897'
parse_idle_time_to_minutes(idle_time)



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




fix_corrupted_video('C:/Users/tools/Argus_demo_dashboard/static/images/cardboard_boxes_7.mp4','C:/Users/tools/Argus_demo_dashboard/static/images/re_cardboard_boxes_7.mp4')