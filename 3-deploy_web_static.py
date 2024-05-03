#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers"""
from fabric.api import env, run, put
from datetime import datetime
import os.path
from pathlib import Path


do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'
env.key_filename = '/root/.ssh/id_rsa'
archive_path = do_pack()


def deploy():
    """Creates and distributes an archive to web servers"""
    if archive_path is None:
        return False
    print("web_static packed: {} -> {}Bytes"
          .format(archive_path, os.path.getsize(archive_path)))
    return do_deploy(archive_path)
