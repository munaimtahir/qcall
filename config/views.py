from django.http import HttpResponse
from django.template.loader import render_to_string


def service_worker(request):
    content = render_to_string("base/service-worker.js")
    return HttpResponse(content, content_type="application/javascript")
