import pdfkit


def to_pdf(html_string, output_file):

    # set up css and options
    css = ['scripts/pdf.css']
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'quiet': '',

    }

    # convert html string to pdf
    pdfkit.from_string(html_string, output_file, options=options, css=css)
