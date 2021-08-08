from django.shortcuts import render
from copy import error
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Q
from datetime import datetime, timezone
from datetime import date
import json
import requests

from .models import  *
from .serializers import *
from .helper import *
import os
from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.
# Create your views here.
@api_view(['GET'])
def ping(request):
    """
    api for pinging if the server is running or not 
    """
    return JsonResponse(
    {
        "success": True
    },
    status=status.HTTP_200_OK
)




@api_view(['GET'])
def getYoutubeData(request):
    if request.method == 'GET':
        videos = videoMetadata.objects.all().order_by("publishedAt").reverse()
        paginator = Paginator(videos, 25) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        pageSerialized = videoMetadataSerializer(page_obj, many=True)
        print(pageSerialized)
        return JsonResponse({'page_obj':pageSerialized.data},safe=False)

@api_view(['GET'])
def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query')
        page_number = request.GET.get('page')
        videos = videoMetadata.objects.filter(
            Q(title__contains=search_query) |
            Q(description__contains=search_query)
        )
        paginator = Paginator(videos, 25) # Show 25 contacts per page.
        
        page_obj = paginator.get_page(page_number)
        pageSerialized = videoMetadataSerializer(page_obj, many=True)
        return JsonResponse({'page_obj':pageSerialized.data},safe=False)


import time

from timeloop import Timeloop
from datetime import timedelta
t1 = Timeloop()

@t1.job(interval=timedelta(seconds=30))
def fetchYoutube():
    url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q=olympics&type=video&"
    
    key = ['key=AIzaSyBje5BbASvYJJrtFJiYvV3ITaDqba1D5uQ','key=AIzaSyC385jui9JLqUH71ZAZjFO_ipOupicrkDI']
    count = videoMetadata.objects.all().count()
    if count%2 == 0:
        url = url+key[count%2]
    else:
        url = url+key[count%2]
    payload={}
    headers = {
    'Authorization': 'AIzaSyBje5BbASvYJJrtFJiYvV3ITaDqba1D5uQ',
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    dataToBeStored = dict()
    for i in data["items"]:
        dataToBeStored["videoId"]=i["id"]["videoId"]
        print(dataToBeStored["videoId"])
        try:
            ans = videoMetadata.objects.get(videoId=dataToBeStored["videoId"])
            print(ans)
        except:
            dataToBeStored["publishedAt"]=i["snippet"]["publishedAt"]
            dataToBeStored["title"] = i["snippet"]["title"]
            dataToBeStored["description"] = i["snippet"]["description"]
            dataToBeStored["thumbnailUrl"] = i["snippet"]["thumbnails"]["default"]["url"]
            videoMetadataSerializerdata = videoMetadataSerializer(data=dataToBeStored)
            if videoMetadataSerializerdata.is_valid():
                print("%%%%%%%%%%%%%%%")
                videoMetadataSerializerdata.save()
    return status.HTTP_201_CREATED
t1.start()