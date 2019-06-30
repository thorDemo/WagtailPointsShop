from wagtail.core import hooks
from django.shortcuts import redirect


@hooks.register('before_serve_document')
def serve_document(document, request):
    # eg. use document.file_extension, document.url, document.filename
    if document.file_extension == 'xls':
        google_view_pdf_base = 'https://docs.google.com/viewer?url='
        # document.url is a relative URL so more work needed here
        # also URL should probably be URL encoded
        redirect_url = google_view_pdf_base + document.url
        # must return an instance of HTTPResponse
        return redirect(redirect_url)
    # no return means the normal page serve will operate
