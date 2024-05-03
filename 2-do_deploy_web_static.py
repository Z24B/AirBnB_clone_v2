#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, put, run
import os

env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = ['/root/.ssh/id_rsa']


def do_deploy(archive_path):
    """Distributes an archive to your web servers and deploys it"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')
        filename = os.path.basename(archive_path)
        folder_name = filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create new link /data/web_static/current linked to new version
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    pass
