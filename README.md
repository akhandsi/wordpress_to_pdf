# WordPress-to-pdf

## Getting Started

### Install Prerequisites
* Install [Homebrew](https://brew.sh/)
* Install [python](https://www.python.org/)

```bash
$ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
$ brew install python3
```

### Install the `wordpress-to-pdf` utilities...

```bash
$ https://github.com/akhandsi/wordpress_to_pdf.git
$ cd wordpress_to_pdf
$ make install
```

## wordpress-to-pdf utilities

### print

The `print` cli allows you to print your wordpress content to pdf.  

```
  Usage: print [options]

  UX Devops Turbo Appliance CLI


  Options:

    --version               output the version number
    --type [content]        content type, eg: Posts, Pages etc.
    --path [file_path]      optional file path to generate the pdf
    --help                  output usage information


  Commands:

    print [options]      prints wordpress content to pdf

  .wordpress-cli.yml: 
  
     YAML file containing the following config options...
     - username: username of the wordpress.com blog
     - password: password of the wordpress.com blog
     - client_id: client id of the wordpress.com blog
     - client_secret: client secret key of the wordpress.com blog
     - site_url: the location of the wordpress.com blog
     
     print will look for .wordpress-cli.yml in the current directory
     and $HOME/.wordpress-cli.yml
```