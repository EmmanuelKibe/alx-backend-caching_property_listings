from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)
def property_list(request):
    # Fetch all properties
    properties = Property.objects.all()
    
    # Prepare data for JsonResponse
    data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": str(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat(),
        }
        for p in properties
    ]
    
    return JsonResponse({"data": data}, safe=False)
