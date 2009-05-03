from django.conf import settings

CACHE_PREFIX = getattr(settings, 'FLATBLOCKS_CACHE_PREFIX', 'flatblocks_')
