from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .movie_query import * 
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render_to_response('index.html')

# Create a view especially to return database value
# Receive a string of binary value 01010101 -> Deduce the category of movies

@csrf_exempt
def search(request):
    if (request.method == 'GET'):
        return HttpResponse('NO GET METHOD')
    elif (request.method == 'POST'):
        # Parse the request data
        try:
            category = request.POST["category"]
        except:
            return HttpResponse("ERROR WITH POST DATA")
        
        # Guarantee that post data is not corrupted (potential XSS)
        if (len(category) != 18):
            return JsonResponse("ERROR WITH POST DATA")

        # Generate the right movie list
        data = perform_movie_query(category)
        return HttpResponse(data)