import threading
from progressbar import ProgressBar, FormatLabel, Bar, Percentage
from time import sleep
import pdf
import wordpress

POST_PER_PAGE = 50
POETRY_CATEGORY_ID = 422


def to_pdf(pdf_file_path):
    # fetch first page, this is needed to get the first header and identify totalPages
    posts = []
    response = wordpress.get_posts_by_page(1, POST_PER_PAGE, POETRY_CATEGORY_ID)
    posts = posts + response["body"]
    total_pages = response["headers"]["X-WP-TotalPages"]
    total_posts = len(response["body"])

    # progress for fetching
    widgets = [FormatLabel('==> Downloaded: {0} posts'.format(total_posts)), ' ', Bar()]
    bar = ProgressBar(widgets=widgets).start()
    page_number = 2

    # fetch all pages
    if total_pages > 1:
        while page_number <= int(total_pages):
            # set bar progress
            if page_number < 100:
                bar.update(page_number)
                sleep(0.1)

            # fetch next page
            response = wordpress.get_posts_by_page(page_number,POST_PER_PAGE, POETRY_CATEGORY_ID)
            posts = posts + response["body"]
            total_posts = total_posts + len(response["body"])

            # update bar labels
            widgets[0] = FormatLabel('==> Downloaded: {0} posts'.format(total_posts))
            page_number = page_number + 1

    bar.finish()

    # parse all posts and create pdf
    convert(posts, pdf_file_path)


def convert(posts, pdf_file_path):
    # set up progress
    widgets = ['==> Converting to pdf:', Percentage(), ' ', Bar()]
    bar = ProgressBar(widgets=widgets).start()

    # set up thread
    thread = threading.Thread(target=pdf.to_pdf, args=(to_html(posts), pdf_file_path,))
    thread.daemon = True
    thread.start()
    i = 1

    # continuous loop till pdf.to_pdf thread is active
    while True:
        # update every second
        if i < 100:
            bar.update(i)
            sleep(1)

        # end of if thread is not alive
        if not thread.is_alive():
            bar.finish()
            break

        i += 1


def to_html(posts):
    html_string = ''

    # append all posts in html string and use css to indicate new page
    for post in posts:
        html_string = html_string + '<h2 class="new-page">' + post["title"][
            "rendered"] + '<br><br><span class="content">' + post["content"][
                          "rendered"] + "</div></h2>"

    return html_string
