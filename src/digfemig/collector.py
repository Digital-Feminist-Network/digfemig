import csv
import json
import os
import time

from instagrapi import Client

from digfemig.login import authenticate


# Media download location setup.
def setup_media_directory(download_path, hashtag):
    full_path = os.path.join(download_path, hashtag)

    # Create the directory if it doesn't exist.
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return full_path


# Download media.
def download_media(hashtag, session_file, download_path, username, password):

    cl = authenticate(session_file, username, password)

    cl.delay_range = [1, 4]

    cl.get_timeline_feed()

    # Metadata file.
    csv_file_path = os.path.join(download_path, f"{hashtag}.csv")

    with open(csv_file_path, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        if os.stat(csv_file_path).st_size == 0:
            csvwriter.writerow(["file_name", "username", "post_url", "caption"])

        timestamp = time.strftime("%Y%m%d%H%M%S")

        medias = cl.hashtag_medias_top(hashtag, amount=100)

        for i, media in enumerate(medias):
            # Grab images and video.
            if media.media_type in {1, 2}:
                padded_index = f"{i:04}"

                file_extension = "jpg" if media.media_type == 1 else "mp4"
                media_filename = (
                    f"{hashtag}-{timestamp}-{padded_index}.{file_extension}"
                )
                media_path = os.path.join(download_path, media_filename)
                post_url = f"https://www.instagram.com/p/{media.code}/"
                ig_username = media.user.username
                ig_caption = media.caption_text

                # Download the media.
                if media.media_type == 1:
                    cl.photo_download_by_url(media.thumbnail_url, media_path)
                elif media.media_type == 2:
                    cl.video_download_by_url(media.video_url, media_path)

                # Write metadata.
                csvwriter.writerow([media_filename, ig_username, post_url, ig_caption])

                image_url = media.thumbnail_url
                image_path = os.path.join(
                    download_path, f"{hashtag}-{timestamp}-{padded_index}"
                )
                cl.photo_download_by_url(image_url, image_path)
