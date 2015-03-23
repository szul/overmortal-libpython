import urlparse

class SubdomainMiddleware(object):
    def process_request(self, request):
        bits = urlparse.urlsplit(request.META['HTTP_HOST'])[0].split('.')
        if(len(bits) == 3):
            request.subdomain = bits[0]
