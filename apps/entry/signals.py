import logging
from django.core.cache import cache
from django.core.cache.backends.base import BaseCache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(post_save)
@receiver(post_delete)
def cache_monitor(sender, **kwargs):
    if isinstance(cache, BaseCache):
        hits = cache._cache.get_stats().get('hits', 0)
        misses = cache._cache.get_stats().get('misses', 0)
        evictions = cache._cache.get_stats().get('evictions', 0)
        # Log cache metrics as INFO level messages
        logger.info(f"Cache hits: {hits}, Cache misses: {misses}, Cache evictions: {evictions}")
