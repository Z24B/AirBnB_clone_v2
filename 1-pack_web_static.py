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
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")

        # Generate archive name 
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None
