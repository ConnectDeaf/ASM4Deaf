import ffmpeg
import glob, os, sys
from my_config import *
from PIL import Image


def generate_all_image_thumbnails():
    for infile in glob.glob(f"{IMAGE_THUMBNAIL_ROOT}*{IMAGE_FILE_FORMAT}"):
        file, ext = os.path.splitext(infile)
        with Image.open(infile) as im:
            im.thumbnail(IMAGE_THUMBNAIL_SIZE)
            im.save(f"{file}{IMAGE_THUMBNAIL_FILE_FORMAT}", "JPEG")

def generate_all_video_thumbnails(): #PENDING

    # for infile in glob.glob(f"{VIDEO_THUMBNAIL_ROOT}*{VIDEO_FILE_FORMAT}"):
    #     file, ext = os.path.splitext(infile)
    #     with Image.open(infile) as im:
    #         im.thumbnail(VIDEO_THUMBNAIL_SIZE)
    #         im.save(f"{file}{VIDEO_THUMBNAIL_FILE_FORMAT}", "MP4")

    pass


if __name__ == "__main__":
    if sys.argv[1] == "images":
        generate_all_image_thumbnails()
    elif sys.argv[1] == "videos":
        generate_all_video_thumbnails()
    else: #both
        generate_all_image_thumbnails()
        generate_all_video_thumbnails()