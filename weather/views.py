from django.shortcuts import render, redirect
import requests
from .forms import City
from .models import RandomCity

import os
from django.conf import settings
from django.http import HttpResponse

def index(request):
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}?unitGroup=uk&key=CCHNQBJPUCVLJVLMQAHZDBSVL&contentType=json'
    city = RandomCity.objects.get(pk=1)
    context = {}
    form = City()
    req = requests.get(url.format(city)).json()
    address = req['address']
    current_date = req['days'][0]['datetime']
    current_temp = req['currentConditions']['temp']
    current_cond = req['currentConditions']['conditions']
    current_cond_icon = req['currentConditions']['icon']
    forecast_datetime = []
    forecast_temp = []
    forecast_desc = []
    forecast_icon = []
    for x in range(1, 15):
        forecast_temp.append(req['days'][x]['temp'])
        forecast_desc.append(req['days'][x]['conditions'])
        forecast_datetime.append(req['days'][x]['datetime'])
        forecast_icon.append(req['days'][x]['icon'])
            
    # Run multiple lists in parallel using the zip() function in template
    forecast_list = zip(forecast_datetime, forecast_temp, forecast_desc, forecast_icon)
    context = {
        'form': form,
        'address': address,
        'current_temp': current_temp,             
        'current_cond': current_cond,
        'current_date': current_date,
        'current_cond_icon': current_cond_icon,
        'forecast_list': forecast_list, 
    }
    if request.method == "POST":
        form = City(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            req = requests.get(url.format(city)).json()

            # Variables to extract
            address = req['address']
            address = address.title()
            current_date = req['days'][0]['datetime']
            current_temp = req['currentConditions']['temp']
            current_cond = req['currentConditions']['conditions']
            current_cond_icon = req['currentConditions']['icon']
            forecast_datetime = []
            forecast_temp = []
            forecast_desc = []
            forecast_icon = []
            
            for x in range(1, 15):
                forecast_temp.append(req['days'][x]['temp'])
                forecast_desc.append(req['days'][x]['conditions'])
                forecast_datetime.append(req['days'][x]['datetime'])
                forecast_icon.append(req['days'][x]['icon'])
            
            # Run multiple lists in parallel using the zip() function in template
            forecast_list = zip(forecast_datetime, forecast_temp, forecast_desc, forecast_icon)

            form = City()

            context = {
                'form': form,
                'address': address,             
                'current_temp': current_temp,             
                'current_cond': current_cond,
                'current_date': current_date,
                'current_cond_icon': current_cond_icon,
                'forecast_list': forecast_list,                       
            }
            # return render(request, 'weather/index.html', context)
            return render(request, 'weather/index.html', context)
    else:
        form = City()
    
    return render(request, 'weather/index.html', context)

# API: https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/osaka?unitGroup=uk&key=CCHNQBJPUCVLJVLMQAHZDBSVL&contentType=json

def ads_txt_view(request):
    with open(os.path.join(settings.STATIC_ROOT, 'ads.txt')) as file:
        file_content = file.readlines()
    return HttpResponse(file_content, content_type="text/plain")