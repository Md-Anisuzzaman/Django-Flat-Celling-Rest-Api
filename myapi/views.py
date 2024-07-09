from django.shortcuts import render
from django.http import HttpResponse
import json
from django.template.loader import get_template

import requests

def users_view(request):
    url = 'http://127.0.0.1:8000/api/projects/'
    response = requests.get(url)
    apidata = response.json()
    context = {
        'projects': apidata
    }
    # context = {
    #     'datas': apidata
    # }
    
    return render(request, 'home.html', context)

# def home(request):
#     context = {'title': 'Jueol Valo chele'}
#     return render(request, 'home.html', context)



def json_view(request):
    data = {'key': 'value'}
    return HttpResponse(json.dumps(data), content_type='application/json')
def pageview(request):
    url = 'http://127.0.0.1:8000/api/projects/3/customers/'
    response = requests.get(url)
    apidata = response.json()
    # context = {
    #     'users': users_data
    # }
    context = {
        'datas': apidata
    }
    return HttpResponse(json.dumps(context), content_type='application/json')