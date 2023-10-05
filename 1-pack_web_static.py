#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """generates a .tgz archive from the contents of the web_static"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_name = 'web_static_{}.tgz'.format(timestamp)
    archive_path = 'versions/{}'.format(archive_name)

    try:
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except Exception:
        return None
