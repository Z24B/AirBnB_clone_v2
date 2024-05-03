#!/usr/bin/python3
"""
Fabric script that distributes an archive to your
web servers using the function do_deploy
"""
from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

# Servers configuration
env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = ['/root/.ssh/id_rsa']


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/
        archive_filename = archive_path.split('/')[-1]
        archive_name_no_ext = archive_filename.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(
                archive_name_no_ext)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move contents of the extracted folder to parent directory
        run("mv {}web_static/* {}".format(release_path, release_path))

        # Delete the now empty web_static directory
        run("rm -rf {}web_static".format(release_path))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    do_deploy()
