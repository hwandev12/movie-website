import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class CacheKeyLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_request(self, request):
        pass
    
    def process_response(self, request, response):
        for key in cache:
            logger.info("Cache key used %s" % key)
        return response