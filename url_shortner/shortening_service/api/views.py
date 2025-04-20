from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from shortening_service.models import ShortenedURL
import random, string
from rest_framework.views import APIView

def shortener_page(request):
    return render(request, 'index.html')  

class CreateShortURL(APIView):

    def post(self, request):
        original_url = request.data.get('url')
        
        if not original_url:
            return Response({"detail": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)
    
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        shortened_url = ShortenedURL.objects.create(url=original_url, shortCode=short_code, createdAt=timezone.now(), updatedAt=timezone.now())
        
        response_data = {
            "id": shortened_url.id,
            "url": original_url,
            "shortCode": short_code,
            "createdAt": shortened_url.createdAt.isoformat(),
            "updatedAt": shortened_url.updatedAt.isoformat()
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class RetrieveShortURL(APIView):

    def get(self, request, pk):
        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)
        except ShortenedURL.DoesNotExist:
            return Response({'message ':'Short code does not exists'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "id": shortened_url.id,
            "url": shortened_url.url,
            "shortCode": shortened_url.shortCode,
            "createdAt": shortened_url.createdAt.isoformat(),
            "updatedAt": shortened_url.updatedAt.isoformat()
        }

        return Response(response_data, status=status.HTTP_200_OK)

# def create_short_url(request):
#     if request.method == "POST":

#         original_url = request.POST.get('url')
#         short_code   = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
#         short_url    = ShortenedURL.objects.create(url=original_url, shortCode=short_code)

#         # return render(request, 'index.html', {
#         #     'short_url': f"{request.get_host()}/{short_url.shortCode}",
#         #     'original_url': original_url
#         # })
#         return render(request, 'index.html',{'short_code': short_code})

#     return render(request, 'index.html')