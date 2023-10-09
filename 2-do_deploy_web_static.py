#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import env, run, put, task
from os.path import exists

env.hosts = ['100.26.20.143', '100.26.237.112']

@task
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

@task
def do_deploy(archive_path):
    """script distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        base_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, base_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, base_name))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, base_name))
        run('rm -rf {}{}/web_static'.format(path, base_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, base_name))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
