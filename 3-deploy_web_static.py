#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = ['/root/.ssh/id_rsa']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        local("mkdir -p versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/" + file_name[:-4]
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        return True
    except:
        return False


def deploy():
    """
    Full deployment
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
