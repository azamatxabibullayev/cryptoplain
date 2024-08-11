from django.shortcuts import render
from .models import FearGreedIndex


def landing_page(request):
    fear_greed_index_image = FearGreedIndex.objects.last()
    context = {
        'fear_greed_index_image': fear_greed_index_image,
    }
    return render(request, 'landing_page.html', context)
