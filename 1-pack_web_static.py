#!/usr/bin/python3
"""generate .tgz archive"""
from fabric.api import local
from datetime import datetime


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
