from django.shortcuts import render
from django.http import HttpResponse
from shortening_service.models import ShortenedURL
import random, string


def create_short_url(request):
    if request.method == "POST":
        # Get the original URL from the form
        original_url = request.POST.get('url')

        # Generate a random short code (you can adjust the length as needed)
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Create a new ShortURL object and save it to the database
        short_url = ShortenedURL.objects.create(url=original_url, shortCode=short_code)

        # Render the response with the new shortened URL
        return render(request, 'index.html', {
            'short_url': f"{request.get_host()}/{short_url.shortCode}",
            'original_url': original_url
        })

    return render(request, 'index.html')