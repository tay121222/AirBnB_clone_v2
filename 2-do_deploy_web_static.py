#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import env, run, put
from os.path import exists

env.hosts = ['100.26.20.143', '100.26.237.112']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


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
