#!/usr/bin/python3


from fabric.api import *
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """

    # Create versions directory if not exist
    local("mkdir -p versions")

    # Create the date format string
    date_string = datetime.now().strftime('%Y%m%d%H%M%S')

    # Set the archive path
    path = "versions/web_static_{}.tgz".format(date_string)

    # Create archive
    status = local("tar -cvzf {} ./web_static/".format(path))

    if status.succeeded:
        return path
    else:
        return None
