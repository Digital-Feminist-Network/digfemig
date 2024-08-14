import logging
import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

# Setup logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler to write logs to a file.
file_handler = logging.FileHandler("digfemig.log")
file_handler.setLevel(logging.INFO)

# Define a simple log format.
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler to the logger.
logger.addHandler(file_handler)


def authenticate(session_file, username, password):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.

    Returns the authenticated Client instance.

    Adapted from https://subzeroid.github.io/instagrapi/usage-guide/best-practices.html
    """

    cl = Client()

    if os.path.exists(session_file):
        session = cl.load_settings(session_file)

        if session:
            try:
                cl.set_settings(session)
                cl.login(username, password)

                # Check if session is valid.
                try:
                    cl.get_timeline_feed()
                    logger.info("Session is valid")
                    return cl
                except LoginRequired:
                    logger.warning(
                        "Session is invalid, need to login via username and password"
                    )

                    # Use the same device UUIDs across logins.
                    old_session = cl.get_settings()
                    cl.set_settings({})
                    cl.set_uuids(old_session["uuids"])

                    # Try and re-login if we fail above.
                    try:
                        cl.login(username, password)
                        logger.info("Re-login successful with the same device UUIDs")
                        return cl
                    except Exception as e:
                        logger.error(f"Re-login failed: {e}")
            except Exception as e:
                logger.error(f"Couldn't login user using session information: {e}")

    # If session login fails, login with username and password.
    try:
        logger.info(
            f"Attempting to login via username and password. username: {username}"
        )
        if cl.login(username, password):
            return cl
    except Exception as e:
        logger.error(f"Couldn't login user using username and password: {e}")

    raise Exception("Couldn't login user with either password or session")
