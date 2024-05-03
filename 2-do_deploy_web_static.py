#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, run, put, sudo, local
from datetime import datetime
from os import path

env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'


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


if __name__ == "__main__":
    do_deploy()
