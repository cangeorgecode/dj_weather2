from django.shortcuts import render, redirect
import requests
from .forms import City

def index(request):
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}?unitGroup=uk&key=CCHNQBJPUCVLJVLMQAHZDBSVL&contentType=json'
    city = ''
    context = {}
    form = City()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = City(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            req = requests.get(url.format(city)).json()

            # Variables to extract
            address = req['address']
            address = address.title()
            current_temp = req['currentConditions']['temp']
            current_cond = req['currentConditions']['conditions']
            # current_cond_icon = req['currentConditions']['icon']
            forecast_datetime = []
            forecast_temp = []
            forecast_desc = []
            
            for x in range(1, 15):
                forecast_temp.append(req['days'][x]['temp'])
                forecast_desc.append(req['days'][x]['description'])
                forecast_datetime.append(req['days'][x]['datetime'])
            
            # Run multiple lists in parallel using the zip() function in template
            forecast_list = zip(forecast_datetime, forecast_temp, forecast_desc)
            context = {
                'form': form,
                'address': address,             
                'current_temp': current_temp,             
                'current_cond': current_cond,
                'forecast_list': forecast_list,                       
            }
            # return render(request, 'weather/index.html', context)
            return render(request, 'weather/index.html', context)
    else:
        form = City()
    
    return render(request, 'weather/index.html', context)
