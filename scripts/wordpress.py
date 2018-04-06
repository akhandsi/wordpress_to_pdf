import sys
import requests
import urllib
import config


def login():

    # fetch yml config
    data = config.fetch()

    print("==> Authenticating to " + data['site_url'])

    # login and handle response
    try:
        response = requests.post("https://wordpress.com/wp-login.php?action=login-endpoint", data=data, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print err
        sys.exit(1)

    return response.json()


def get_posts_by_page(page, post_per_page, post_category_id):

    # fetch yml config
    config_props = config.fetch()
    args = {"page": page, "_envelope": "1", 'per_page': post_per_page, 'categories': post_category_id}
    url = "https://public-api.wordpress.com/wp/v2/sites/" + config_props["site_url"] + "/posts?{}".format(
        urllib.urlencode(args))

    # fetch post and handle response
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print err
        sys.exit(1)

    return response.json()
