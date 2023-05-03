#!/usr/bin/python3


from fabric.api import *
import os


env.hosts = ['54.237.86.166', '54.236.48.218']
env.user = 'ubuntu'


def do_clean(number=0):
    """Deletes outdated archives"""

    # Check if versions directory exists
    if os.path.isdir('versions'):
        # Get a list of archives in the directory
        archive_list = os.listdir('versions')

    # Remove the most recent archive from the list
    archive_list.remove(max(archive_list))

    # Check if more than one latest archive is required
    if number > 1:
        # Remove the second most recent archive from the list
        archive_list.remove(max(archive_list))

    # Delete outdated archives locally
    for archive in archive_list:
        if 'web_static_' in archive:
            local('rm versions/{}'.format(archive))

    # Get a list of archives from server
    archive_list = run('ls -t /data/web_static/releases/').split()

    # Remove the latest version of archive from list
    archive_list.remove(max(archive_list))

    # Check if more than one archive is required
    if number > 1:
        # Remove the second most recent archive from list
        archive_list.remove(max(archive_list))

    # Delete outdated archives from servers
    for archive in archive_list:
        if 'web_static_' in archive:
            sudo('rm -rf /data/web_static/releases/{}'.format(archive))
