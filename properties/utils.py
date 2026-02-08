from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Attempt to retrieve data from Redis
    properties = cache.get('all_properties')

    if properties is None:
        # Cache miss: Fetch from PostgreSQL
        properties = list(Property.objects.all())
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties