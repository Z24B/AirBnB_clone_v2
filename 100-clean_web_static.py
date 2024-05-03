#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
import os
from fabric.api import cd, env, local, run

env.hosts = ['100.26.240.110', '54.157.160.220']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    n = 1 if int(number) == 0 else int(number)
    files = [f for f in os.listdir('./versions')]
    files.sort(reverse=True)
    for f in files[n:]:
        local("rm -f versions/{}".format(f))
    remote = "/data/web_static/releases/"
    with cd(remote):
        tgz = run(
            "ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'"
        ).split()
        tgz.sort(reverse=True)
        for d in tgz[n:]:
            run("rm -rf {}{}".format(remote, d))
