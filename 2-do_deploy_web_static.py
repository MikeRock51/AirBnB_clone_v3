#!/usr/bin/python3
from fabric.api import *
import os


# List of hosts and users
env.hosts = ['54.237.86.166', '54.236.48.218']
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to web servers"""

    if not os.path.exists(archive_path):
        return False

    # Copy archive to server
    status = put(archive_path, "/tmp/")
    if not status.succeeded:
        return False

    # Extract archive file name
    arc = archive_path.split('/')[-1].strip('.tgz')

    # Destination path for archive extraction
    dest_folder = "/data/web_static/releases/{}/".format(arc)

    # Extract archive file name
    arc = archive_path.split('/')[-1].strip('.tgz')

    # Create archive extration path
    status = sudo("mkdir {} -p".format(dest_folder))
    if not status.succeeded:
        return False

    # Extract archive to destination folder
    status = sudo("tar -xzvf /tmp/{}.tgz -C {}".format(arc, dest_folder))
    if not status.succeeded:
        return False

    # Move archive content to archive web_static_version directory
    status = sudo("mv {}web_static/* {}".format(dest_folder, dest_folder))
    if not status.succeeded:
        return False

    # Delete emptied archive folder
    status = sudo("rm -rf {}/web_static/".format(dest_folder))
    if not status.succeeded:
        return False

    # Delete archive from server
    status = sudo("rm /tmp/{}.tgz".format(arc))
    if not status.succeeded:
        return False

    # Delete old symbolic link from server
    status = sudo("rm -rf /data/web_static/current")
    if not status.succeeded:
        return False

    # Create new symbolic link
    status = sudo("ln -s {} /data/web_static/current".format(dest_folder))
    if not status.succeeded:
        return False

    return True
