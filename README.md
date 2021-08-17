# WordPress-to-pdf

## Getting Started

### Install Prerequisites
* Install [Homebrew](https://brew.sh/)
* Install [python](https://www.python.org/)

```bash
$ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
$ brew install python3
$ brew install Caskroom/cask/wkhtmltopdf
$ pip3 install virtualenv
```

### Install the `wordpress-to-pdf` utilities...

```bash
$ https://github.com/akhandsi/wordpress_to_pdf.git
$ cd wordpress_to_pdf
$ make install
```

## wordpress-to-pdf utilities

### wordpress-print

The `wordpress-print` cli allows you to print your wordpress content to pdf.  

```
  Usage: venv/bin/wordpress-print [options]

  Options:

    --version               output the version number
    --type [content]        content type, eg: Posts, Pages etc.
    --path [file_path]      optional file path to generate the pdf
    --help                  output usage information


  Commands:

    wordpress-print [options]         prints wordpress content to pdf

  .wordpress-cli.yml:

     YAML file containing the following config options...
     - username: username of the wordpress.com blog
     - password: password of the wordpress.com blog
     - client_id: client id of the wordpress.com blog
     - client_secret: client secret key of the wordpress.com blog
     - site_id: the id of the wordpress.com blog
     - post_category_id: the id of the wordpress.com post type that you want to print
     - home_page_id: the id of the wordpress.com blog home page. This would be used for adding cover information

     print will look for .wordpress-cli.yml in the current directory
     and $HOME/.wordpress-cli.yml
```

*client_id, client_secret can be retrieved via https://developer.wordpress.com/docs/api/console/
