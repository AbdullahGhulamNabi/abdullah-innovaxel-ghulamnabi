from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from shortening_service.models import ShortenedURL
import random, string
from rest_framework.views import APIView
from .serializers import ShortenedURLSerializer

def shortener_page(request):
    return render(request, 'index.html')  

class ShortURLAPIView(APIView):

    def post(self, request):

        '''
            api for creating a short url 
        '''

        try:
            serializer = ShortenedURLSerializer(data=request.data)

            if serializer.is_valid():
                short_code    = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                shortened_url = ShortenedURL.objects.create(
                    url=serializer.validated_data['url'],
                    shortCode=short_code,
                    createdAt=timezone.now(),
                    updatedAt=timezone.now()
                )

                response_serializer = ShortenedURLSerializer(shortened_url)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):

        '''
            api for retreving the original url using shortcode from short url
        '''

        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)  
            shortened_url.accessCount += 1
            shortened_url.save() 
            
            serializer = ShortenedURLSerializer(shortened_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ShortenedURL.DoesNotExist:
            return Response({'message':'Short code does not exists'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):

        '''
            api for updating the origional url against the new hortcode
        '''

        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)
        except ShortenedURL.DoesNotExist:
            return Response({'message': 'Short code does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShortenedURLSerializer(shortened_url, data=request.data)
        if serializer.is_valid():
            serializer.save(updatedAt=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        '''
            api for deleting the short url stored in database
        '''

        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)
            shortened_url.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except ShortenedURL.DoesNotExist:
            return Response({'message': 'Short code does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class StatsURLAPIView(APIView):
    def get(self, request, pk):

        '''
            api for showing the stats of the accessed short url
        '''

        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)
            serializer = ShortenedURLSerializer(shortened_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ShortenedURL.DoesNotExist:
            return Response({'message': 'Short code does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

class RedirectToOriginalURL(APIView):
    def get(self, request, pk):

        '''
            api for redirecting to original url when the short url is hit in browser
        '''

        try:
            shortened_url = ShortenedURL.objects.get(shortCode=pk)
            return redirect(shortened_url.url, permanent=True)
        except ShortenedURL.DoesNotExist:
            return Response({'message': 'Short code does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)