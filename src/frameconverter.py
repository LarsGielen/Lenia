import cv2 as cv
import numpy as np
import argparse
import sys

def read_txt_file(file_path, verbose=False):
    with open(file_path, 'r') as file:
        settings_line = file.readline().strip()
        
        settings = dict(setting.split(':') for setting in settings_line.split(' '))
        width = int(settings['width'])
        height = int(settings['height'])
        frame_amount = int(settings['frames'])
        
        frames = [[0.0] * width * height] * frame_amount
        for i, line in enumerate(file):
            frames[i] = [float(value.strip()) for value in line.strip().split(';') if value]
            if verbose: print_progress_bar(f"reading file {file_path}", i + 1, frame_amount)
        frames = frames.reshape((frame_amount, height, width))
        
    return width, height, frame_amount, frames

def read_bin_file(file_path, verbose=False):
    with open(file_path, 'rb') as file:
        if verbose: print_progress_bar(f"reading file {file_path}", 1, 5)
        width = np.fromfile(file, dtype=np.uint64, count=1)[0]
        if verbose: print_progress_bar(f"reading file {file_path}", 2, 5)
        height = np.fromfile(file, dtype=np.uint64, count=1)[0]
        if verbose: print_progress_bar(f"reading file {file_path}", 3, 5)
        frame_amount = np.fromfile(file, dtype=np.uint64, count=1)[0]
        if verbose: print_progress_bar(f"reading file {file_path}", 4, 5)
        frames = np.fromfile(file, dtype=np.float32)
        if verbose: print_progress_bar(f"reading file {file_path}", 5, 5)

    frames = frames.reshape((frame_amount, height, width))
    return width, height, frame_amount, frames

def create_normalized_image(width, height, frame, image_output_path, verbose):
    frame_image = np.zeros((height, width, 3), dtype=np.uint8)
    frame /= np.max(frame)
    for x in range(width):
        for y in range(height):
            intensity = frame[x + y * width]
            pixel_value = min(max(intensity * 255, 0), 255)
            frame_image[x, y] = (pixel_value, pixel_value, pixel_value)

    if verbose: print_progress_bar(f"Creating image {image_output_path}", 1, 1)
    cv.imwrite(image_output_path, frame_image)
    
def create_video(width, height, frames, framerate, frame_skip, video_output_path, verbose):
    if verbose: print_progress_bar(f"Creating video {video_output_path}", 0, len(frames))
    video_writer = cv.VideoWriter(video_output_path, cv.VideoWriter_fourcc(*'mp4v'), int(framerate), (width, height))
    for i in range(0, frames.shape[0], frame_skip):
        frame_image = np.zeros((height, width, 3), dtype=np.uint8)
        intensity = frames[i]
        frame_image[:] = (255, 255, 255) 

        frame_image[(intensity > 0.9000)] = (85, 0, 187)
        frame_image[(intensity > 0.8000) & (intensity <= 0.9)] = (255, 0, 255)
        frame_image[(intensity > 0.7000) & (intensity <= 0.8)] = (255, 34, 221)
        frame_image[(intensity > 0.6000) & (intensity <= 0.7)] = (255, 102, 153)
        frame_image[(intensity > 0.5000) & (intensity <= 0.6)] = (255, 119, 102)
        frame_image[(intensity > 0.4000) & (intensity <= 0.5)] = (255, 136, 51)
        frame_image[(intensity > 0.3000) & (intensity <= 0.4)] = (255, 153, 0)
        frame_image[(intensity > 0.2000) & (intensity <= 0.3)] = (255, 187, 51)
        frame_image[(intensity > 0.1000) & (intensity <= 0.2)] = (255, 221, 102)
        frame_image[(intensity > 0.0001) & (intensity <= 0.1)] = (255, 255, 153)

        if verbose and i + 1 < frames.shape[0]: print_progress_bar(f"Creating video {video_output_path}", i + 1, frames.shape[0])
        video_writer.write(frame_image)
    if verbose: print_progress_bar(f"Creating video {video_output_path}", frames.shape[0], frames.shape[0])
    video_writer.release()

def print_progress_bar(title, current, total, bar_width=50):
    if ((current - 1) / total) * 100.0 >= int(current / total * 100.0):
        return

    progress = current / total
    pos = int(bar_width * progress)
    bar = f"{title}: [{'=' * pos}{'>' if pos < bar_width else ''}{' ' * (bar_width - pos - 1)}] {int(progress * 100)}%"
    
    sys.stdout.write(f"\r{bar}")
    if current == total: print("")
    sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from frame data.")
    parser.add_argument("-i", "--input_file", default="input", help="Path to the input txt file containing frame data")
    parser.add_argument("-o", "--output_file", default="output", help="Path to the output file")
    parser.add_argument("-s", "--frame_skip", default=1, help="How many frames to skip to reduce computation time")
    parser.add_argument("--output_type", default="mp4", help="Type of output (mp4 or jpg)")
    parser.add_argument("--output_framerate", default=10, help="Framerate of the mp4 file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    width, height, frame_amount, frames = read_bin_file(args.input_file + ".bin", verbose=args.verbose)
    if args.output_type == "mp4": create_video(width, height, frames, args.output_framerate, int(args.frame_skip), args.output_file + "." + args.output_type, args.verbose)
    if args.output_type == "jpg": create_normalized_image(width, height, frames[0], args.output_file + "." + args.output_type, args.verbose)

    
