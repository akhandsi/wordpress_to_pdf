#!/usr/bin/env python
import webbrowser
import os
from os.path import expanduser
import urllib3
import click
from . import __version__ as VERSION
import scripts.auth
import scripts.posts


@click.command()
@click.option('--type', default='posts', help='Type of wordpress content')
@click.option('--path', default='', help='destination of pdf file')
@click.version_option(version=VERSION)
def main(type, path):

    # disable all html certificate warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # login to the given site_url
    scripts.auth.login()

    # add a default path for pdf to be generated
    home = expanduser("~")
    default_file_path = home + '/Desktop/blogBook.pdf'

    if path == '':
        path = default_file_path

    # generate pdf from posts
    scripts.posts.to_pdf(path)

    print("==> PDF generated at [ " + os.path.realpath(path) + " ]")

    # open generated pdf
    webbrowser.open('file://' + os.path.realpath(path))


if __name__ == '__main__':
    main()
