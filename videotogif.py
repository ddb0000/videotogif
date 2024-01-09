import subprocess
import time

def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True)
        print("command executed successfully")
    except subprocess.CalledProcessError as e:
        print("an error occurred:", e)

def video_to_gif():
    original_file_path = input("enter the path of the video file: ").strip('\"')

    compression_type = input("choose compression type (soft/hard): ").lower() or 'hard'
    scale, fps = ("scale=800:450", "fps=15") if compression_type == "soft" else ("scale=640:360", "fps=10")

    filters = [scale, fps]

    if input("do you want to change video speed? (y/N): ").lower() == 'y':
        speed_factor = input("enter speed factor (e.g., 2 for double speed): ")
        filters.append(f"setpts=(1/{speed_factor})*PTS")

    if input("do you want to crop the video? (y/N): ").lower() == 'y':
        crop_top = input("enter the number of pixels to crop from the top: ")
        crop_bottom = input("enter the number of pixels to crop from the bottom: ")
        crop_left = input("enter the number of pixels to crop from the left: ")
        crop_right = input("enter the number of pixels to crop from the right: ")
        filters.append(f"crop=in_w-{int(crop_left)+int(crop_right)}:in_h-{int(crop_top)+int(crop_bottom)}:{crop_left}:{crop_top}")

    filter_complex_str = ','.join(filters)

    trim_cmd = []
    if input("do you want to trim the video? (y/N): ").lower() == 'y':
        start_time = input("enter the start time for trimming (in seconds): ")
        end_time = input("enter the end time for trimming (in seconds): ")
        trim_cmd = ["-ss", start_time, "-to", end_time]

    gif_filename = original_file_path.rsplit('.', 1)[0] + '.gif'
    ffmpeg_command = ["ffmpeg", "-i", original_file_path] + trim_cmd + ["-vf", filter_complex_str, "-an", "-y", gif_filename]

    start_time = time.time()
    run_ffmpeg_command(ffmpeg_command)
    end_time = time.time()
    print(f"successfully converted the video to gif. saved as {gif_filename} | time taken: {end_time - start_time:.2f} seconds")

video_to_gif()
