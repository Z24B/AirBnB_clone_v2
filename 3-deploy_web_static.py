#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers"""
from fabric.api import env, run, put
from datetime import datetime
from os import path
from pathlib import Path

env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        local("mkdir -p versions")
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
                now.year, now.month, now.day, now.hour, now.minute, now.second)
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        name = archive_path.split('/')[1].split('.')[0]
        sudo("mkdir -p /data/web_static/releases/{}/".format(name))
        sudo("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
             .format(name, name))
        run("rm /tmp/{}.tgz".format(name))
        sudo("mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/".format(name, name))
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(name))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current"
             .format(name))
        return True
    except Exception:
        return False
