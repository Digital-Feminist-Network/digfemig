import csv
import json
import os
import time

from instagrapi import Client

# Credentials
USERNAME = ""
PASSWORD = ""
SESSION_FILE = "session.json"

# Hashtag to search for.
HASHTAG = ""
IMAGE_DIR = ""

# Media download location setup.
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


# Cache session.
def save_session(cl):
    with open(SESSION_FILE, "w") as f:
        json.dump(cl.get_settings(), f)

# Load session from cache.
def load_session(cl):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            settings = json.load(f)
            cl.set_settings(settings)
        cl.login(USERNAME, PASSWORD)
        return True
    return False


# Download media
def download_images():
    # Initialize a login client.
    cl = Client()

    # Load session if available, otherwise login and save session.
    if not load_session(cl):
        cl.login(USERNAME, PASSWORD)

        save_session(cl)

    # Metadata file.
    csv_file_path = os.path.join(IMAGE_DIR, f"{HASHTAG}.csv")

    with open(csv_file_path, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        if os.stat(csv_file_path).st_size == 0:
            csvwriter.writerow(["file_name", "username", "post_url"])

        timestamp = time.strftime("%Y%m%d%H%M%S")

        medias = cl.hashtag_medias_recent(HASHTAG, amount=100)

        for i, media in enumerate(medias):
            # Grab images and video.
            if media.media_type in {1, 2}:
                padded_index = f"{i:04}"

                file_extension = "jpg" if media.media_type == 1 else "mp4"
                media_filename = (
                    f"{HASHTAG}-{timestamp}-{padded_index}.{file_extension}"
                )
                media_path = os.path.join(IMAGE_DIR, media_filename)
                post_url = f"https://www.instagram.com/p/{media.code}/"
                username = media.user.username

                # Download the media
                if media.media_type == 1:
                    cl.photo_download_by_url(media.thumbnail_url, media_path)
                elif media.media_type == 2:
                    cl.video_download_by_url(media.video_url, media_path)

                # Write metadata
                csvwriter.writerow([media_filename, username, post_url])

                image_url = media.thumbnail_url
                image_path = os.path.join(
                    IMAGE_DIR, f"{HASHTAG}-{timestamp}-{padded_index}"
                )
                cl.photo_download_by_url(image_url, image_path)


if __name__ == "__main__":
    download_images()
