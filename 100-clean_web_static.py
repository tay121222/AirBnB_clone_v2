#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import env, run, put, local, cd
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.20.143', '100.26.237.112']


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


def do_deploy(archive_path):
    """script distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_filename = archive_path.split('/')[-1].split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_filename))
        run('tar -xzf /tmp/{}.tgz '
            '-C /data/web_static/releases/{} '
            '--strip-components=1'.format(
                archive_filename, archive_filename
                )
            )
        run('rm /tmp/{}.tgz'.format(archive_filename))
        run('rm -f /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(archive_filename))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    """deletes out-of-date archives"""
    number = int(number)
    if number < 2:
        number = 1

    number_keep = number + 1

    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs rm -rf'.format(number_keep))
    path = '/data/web_static/releases'
    with cd(path):
        run('ls -t | tail -n +{} | xargs rm -rf'.format(number_keep))
