from django.template import loader, RequestContext, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings

def flatfilepage(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if url == '/' or url == '':
        url = 'index.html'
    elif url.startswith('/'):
        url = url[1:-1] + '.html'
    else:
        url = url[:-1] + '.html'
    try:
        t = loader.get_template(url)
        c = RequestContext(request, {
            'flatfilepage': url,
            'request': request
        })
    except TemplateDoesNotExist:
        raise Http404('No template matches %s in the template loading path.' % url)
    response = HttpResponse(t.render(c))
    return response
