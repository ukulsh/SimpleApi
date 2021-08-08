from rest_framework import status
from django.http.response import JsonResponse
from django.shortcuts import render
from copy import error

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from datetime import datetime

from datetime import datetime, timezone



import aiohttp
import time
import asyncio
from .models import  *
from .serializers import *
# Create your views here.
# Create your views here.
def sorting(sortBy,direction,data):
    """
    helper sorting function, The sortBy parameter specifies which field should be used to sort the returned
    results. This is an optional parameter, with a default value of `id`.
    The direction parameter specifies if the results should be returned in ascending
    order (if the value is "asc") or descending order (if the value is "desc"). The default
    value of the direction parameter is `asc`. 
    """
    if sortBy not in ("id","reads","popularity","likes"):
        return 0
    if direction == "asc":
        sortedResult = sorted(data, key = lambda i: i[sortBy])
    elif direction == "desc":
        sortedResult = sorted(data, key = lambda i: i[sortBy],reverse=True)
    
    return sortedResult


async def get_json_data(session, url):
    async with session.get(url) as res:
        json_data = await res.json()
        return json_data

async def getData(tags):
    tagArray = tags.split(",")
    tagArray = list(filter(None, tagArray))

    actions = []
    data_json = []
    id_set = set()
    #Using the set data strcture to filter out results that are already existing based on another tag, it saves time and space for large amount of values
    
    #getting the data from multiple urls in an asynchronous manner, using aiohttp for creating sessions and collecting the pooled data into the api_res variable
    async with aiohttp.ClientSession() as session:
        for tag in tagArray:
            url = f"https://api.hatchways.io/assessment/blog/posts?tag={tag}"
            print(url)
            actions.append(asyncio.ensure_future(get_json_data(session, url)))
        
        api_res = await asyncio.gather(*actions)
        print(api_res)
        for i in api_res:
            for metadata in (i["posts"]):
                if metadata["id"] not in id_set:
                    # appending the data and adding id in the set so that only unique metadata get's stored in the variable
                    data_json.append(metadata)
                    id_set.add(metadata["id"])
    return data_json