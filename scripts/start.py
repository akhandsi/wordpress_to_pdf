#!/usr/bin/env python
import webbrowser
import os
from os.path import expanduser
import urllib3
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
# from . import __version__ as VERSION
import scripts.wordpress


@click.command(cls=HelpColorsCommand, help_options_color='yellow')
@click.option('--path', default='', help='destination of pdf file')
# @click.version_option(version=VERSION)
def main(path):
    # disable all html certificate warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # add a default path for pdf to be generated
    home = expanduser("~")
    default_file_path = home + '/Desktop/blogBook.pdf'

    if path == '':
        path = default_file_path

    # -----------------------------------------------------------------

    # create instance of the wordPress utility class
    wordpress_utility_instance = scripts.wordpress.WordpressUtility()

    # generate pdf from posts
    wordpress_utility_instance.download_to_pdf(path)

    print("==> PDF generated at [ " + os.path.realpath(path) + " ]")

    # -----------------------------------------------------------------
    # open generated pdf
    webbrowser.open('file://' + os.path.realpath(path))


if __name__ == '__main__':
    main()
