#!/usr/bin/python3
"""generate .tgz archive"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import isfile


env.hosts = ["34.73.118.176", "3.90.108.205"]


def do_pack():
    """create a tgz file"""
    # create folder if not exists
    local("mkdir -p versions")
    # create tgz file name
    now = datetime.now()
    tgz_arc = "versions/web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))
    tgzCommand = "tar -cvzf {} web_static".format(tgz_arc)
    # return de path
    if local(tgzCommand) == 1:
        return None
    return tgz_arc


def do_deploy(archive_path):
    """deploy archive to the web servers"""
    # check the path
    if isfile(archive_path) is False:
        return False

    first = archive_path.split('/')
    second = first[1].split(".")
    file_ = second[0]

    try:
        put(archive_path, '/tmp')
        run("sudo mkdir -p /data/web_static/releases/" + file_ + "/")
        run("sudo tar -xzf /tmp/" + file_ + ".tgz" +
            " -C /data/web_static/releases/" + file_ + "/")
        run("sudo rm /tmp/" + file_ + ".tgz")
        run("sudo mv /data/web_static/releases/" + file_ +
            "/web_static/* /data/web_static/releases/" + file_ + "/")
        run("sudo rm -rf /data/web_static/releases/" + file_ + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/" + file_ +
            "/ /data/web_static/current")
    except Exception:
        return False

    return True
