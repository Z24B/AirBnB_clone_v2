#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os.path


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        # Create the versions directory if it doesn't exist
        local("mkdir -p versions")

        # Generate archive name
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
                now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Compress web_static folder into archive
        local("tar -cvzf versions/{} web_static".format(archive_name))

        # Return archive path if successfully generated
        return "versions/{}".format(archive_name)
    except Exception:
        return None

if __name__ == "__main__":
    do_pack()
