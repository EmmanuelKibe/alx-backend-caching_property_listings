from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

def get_all_properties():
    # Attempt to retrieve data from Redis
    properties = cache.get('all_properties')

    if properties is None:
        # Cache miss: Fetch from PostgreSQL
        properties = list(Property.objects.all())
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        con = get_redis_connection("default")
        info = con.info()

        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses

        # Calculate ratio using total_requests
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }

        logger.info(f"Redis Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Failed to retrieve Redis metrics: {e}")
        return {"error": "Could not retrieve metrics"}