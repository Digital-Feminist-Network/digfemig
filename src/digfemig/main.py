import argparse
import os
import sys

import tomli

from digfemig import collector, login


def parse_arguments():
    parser = argparse.ArgumentParser(description="DigFemNet Instagram Bulk Collector")
    parser.add_argument("config", help="Path to the digfemig.toml configuration file")
    return parser.parse_args()


def read_config(file_path):
    with open(file_path, "rb") as f:
        config = tomli.load(f)
    return config


def main():
    config = read_config("digfemig.toml")


def main():
    config = read_config("digfemig.toml")

    # Extract settings from the config.
    hashtag = config.get("settings", {}).get("hashtag", "")
    session_file = config.get("settings", {}).get("session_file", "")
    username = config.get("settings", {}).get("username", "")
    password = config.get("settings", {}).get("password", "")
    download_path = config.get("settings", {}).get("download_path", "")

    # Log in to Instagram.
    cl = login.authenticate(session_file, username, password)

    # Setup the media directory.
    media_directory = collector.setup_media_directory(download_path, hashtag)

    # Download media using the collector module.
    collector.download_media(
        hashtag=hashtag,
        session_file=session_file,
        download_path=media_directory,
        username=username,
        password=password,
    )


if __name__ == "__main__":
    main()
