import sys
import requests
import urllib
from time import sleep
from progressbar import ProgressBar, FormatLabel, Bar
import pdfkit
import scripts.config

pdf_css = ['scripts/css/pdf.css']
pdf_options = {
    'page-size': 'A4',
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8',
    'quiet': '',
}


# WordpressUtility is a class to perform various wordPress related operations
class WordpressUtility:
    __data = []

    # constructor
    def __init__(self):
        self.__data = {k: v for d in scripts.config.fetch() for k, v in d.items()}
        self.__authenticate()

    # authenticate to wordPress developer portal
    def __authenticate(self):
        try:
            response = \
                requests.post('https://wordpress.com/wp-login.php?action=login-endpoint'
                              , data=self.__data, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        return response.json()

    # fetch all posts for the given page
    def __fetch_home_page(self):
        try:
            url = 'https://public-api.wordpress.com/wp/v2/sites/{0}/pages/{1}'.format(str(self.__data['site_id']),
                                                                                      self.__data['home_page_id'])
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        return response.json()

    # fetch all posts for the given page
    def __fetch_posts(self, page_number):
        try:
            args = {
                'page': page_number,
                '_envelope': '1',
                'per_page': 20,
                'categories': self.__data['post_category_id'],
            }
            url = 'https://public-api.wordpress.com/wp/v2/sites/{0}/posts?_embed=author,wp:term&{1}'.format(
                str(self.__data['site_id']), urllib.parse.urlencode(args))
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        return response.json()

    # download wordPress content to provided pdf file
    def download_to_pdf(self, pdf_file_path):

        # fetch first page, this is needed to get the first header and identify totalPages
        posts = []
        page_number = 1
        response = self.__fetch_posts(page_number)
        posts = posts + list(response['body'])
        total_pages = int(response['headers']['X-WP-TotalPages'])
        total_posts = int(response['headers']['X-WP-Total'])

        # progress for fetching
        widgets = [FormatLabel('==> Fetching: {0} posts'.format(total_posts)), ' ', Bar()]
        bar = ProgressBar(widgets=widgets, max_value=total_posts).start()
        page_number = page_number + 1

        # if we got multiple pages then start showing the progress
        if total_pages > 1:
            while page_number <= int(total_pages):
                # set bar progress
                if page_number < 100:
                    bar.update(page_number, force=True)
                    sleep(0.1)

                # fetch next page
                response = self.__fetch_posts(page_number)

                # append to available posts
                posts = posts + list(response['body'])

                # update progress labels
                widgets[0] = FormatLabel('==> Fetching: {0} posts'.format(total_posts))

                # update page number to fetch
                page_number = page_number + 1

        bar.finish()

        # once all posts are fetched, convert to html and start exporting to pdf
        widgets2 = [FormatLabel('==> Exporting: {0} posts'.format(len(posts))), ' ', Bar()]
        bar2 = ProgressBar(widgets=widgets2, max_value=len(posts)).start()

        # create User information from first post as first page of pdf
        user_info_html_string = WordpressHtmlUtility.to_formatted_html_author_info(posts[0], self.__fetch_home_page())

        # convert all posts to html string for rest of the pages of the pdf
        posts_html_string = ''
        for i in range(len(posts)):
            posts_html_string = posts_html_string + WordpressHtmlUtility.to_formatted_html_post(posts[i])
            bar2.update(i, force=True)

        bar2.finish()

        # combine all html strings together for a single pdf
        html_string = """{0} {1}""".format(user_info_html_string, posts_html_string)

        # convert html string to pdf
        pdfkit.from_string(html_string, pdf_file_path, options=pdf_options, css=pdf_css)


# WordpressHtmlUtility is a class to handle html formatting for every posts
class WordpressHtmlUtility:

    @staticmethod
    def to_formatted_html_author_info(first_post, home_page):
        home_page_description = home_page['content']['rendered']
        user_info = first_post['_embedded']['author'][0]
        avatar_urls = user_info['avatar_urls']
        description = user_info['description'].replace('\n', '<br>')
        link = user_info['link']
        return """<div class="new-page">
                        <div class="container">
                            <div class="row">
                                <div class="column">
                                    <img src="{0}"/>
                                </div>
                                <div class="column">
                                    <span>{1}<br><br><a href="{2}">{2}</a></span>
                                </div>
                            </div>
                            <br>
                            <hr>
                            <br>
                            <div class="content">
                                {3}
                            </div>
                       </div>
                </div>""".format(avatar_urls['96'], description, link, home_page_description)

    @staticmethod
    def to_formatted_html_post(post):
        title = post['title']
        content = post['content']
        rendered_title = title['rendered']
        rendered_content = content['rendered'].replace('\n', '').replace('div', 'p').replace(
            ' style="margin-top:20px;"', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p></p>',
                                                                                                          '').replace(
            '<p>&nbsp;</p>', '')
        return """<div class="new-page">
                    <h2>{0}</h2>
                    <br><br>
                    <div class="content">
                        {1}
                    </div>
               </div>""".format(rendered_title, rendered_content)
