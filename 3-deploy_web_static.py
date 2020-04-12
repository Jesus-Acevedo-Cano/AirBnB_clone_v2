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

    try:
        fullName = archive_path.split("/")[1]
        fileName = archive_path.split("/")[1].split(".")[0]
        # upload file in /tmp/
        put(archive_path, "/tmp/{}".format(fullName))
        # create the directory to uncompress
        cmd = "sudo mkdir -p /data/web_static/releases/{}/".format(fileName)
        run(cmd)
        # uncompress file
        cmd = "sudo tar -xzf /tmp/{} -C ".format(fullName)
        cmd += "/data/web_static/releases/{}/".format(fileName)
        run(cmd)
        # delete file from server
        cmd = "sudo rm /tmp/{}".format(fullName)
        run(cmd)
        # move files
        cmd = "sudo mv /data/web_static/releases/{}".format(fileName)
        cmd += "/web_static/* "
        cmd += "/data/web_static/releases/{}/".format(fileName)
        run(cmd)
        # delete folder
        cmd = "sudo rm -rf /data/web_static/releases/{}".format(fileName)
        cmd += "/web_static"
        run(cmd)
        # delete symlink
        cmd = "sudo rm -rf /data/web_static/current"
        run(cmd)
        # new symlink
        cmd = "sudo ln -s /data/web_static/releases/{}/ ".format(fileName)
        cmd += "/data/web_static/current"
        run(cmd)
    except Exception:
        return False
    return True


def deploy():
    """create and deploy to all servers"""
    _file = do_pack()
    if _file is None:
        return False
    return do_deploy(_file)
