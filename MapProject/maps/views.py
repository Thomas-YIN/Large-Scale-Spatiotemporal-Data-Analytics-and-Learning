import pandas as pd
import io
import math
import copy
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from maps.models import *

# from maps.models import Document
from .forms import *
import json



# Create your views here.
def home_view(request):
    return render(request, "Map.html", {})


def csv_upload_view(request):
    if request.method == "POST":
        form = TableForm(request.POST, request.FILES)
    else:
        form = TableForm()

    if form.is_valid():
        form.save()
        form = TableForm()

    context = {
        "form": form,
    }
    return render(request, "upload.html", context)


def pop_density_view(request):
    # Load data from model GeoJsonFile
    data = Json.objects.filter(geojson_file="data/json/PopulationDensityData.json")[0]
    statesData = json.load(data.geojson_file)

    return render(
        request, "PopulationDensity.html", {"statesData": json.dumps(statesData)}
    )


def median_income_view(request):

    data = Json.objects.filter(geojson_file="data/json/IncomeData.json")[0]
    statesPoint = json.load(data.geojson_file)

    return render(
        request, "MedianIncome.html", {"statesPoint": json.dumps(statesPoint)}
    )


def data_overview(request):
    # render all uploaded data as a list for user to choose from
    all_data = []
    for table in Table.objects.all():
        
        all_data.append(table)

    # data_form = DataForm()
    return render(
        request, "DataOverview.html", {"data_list": all_data, "len": len(all_data)}
    )

# Geojson templates as dicts
FEATURE_COLLECTION_TEMPLATE = {
    "type": "FeatureCollection",
    "features": []
}

FEATURE_TEMPLATE = {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "type": "",
          "coordinates": []
        }
}

def generic_data_view(request, filename):

    data = Table.objects.filter(table_data=("data/csv/" + filename))[0]
    '''
    Generate geojson file at runtime
    '''
    df = pd.read_csv(io.StringIO(data.table_data.read().decode('utf-8')), delimiter=',')
    '''
    Iterate through all entries by rows (each row stores the data for one admin area)
    '''
    feature_collection = copy.deepcopy(FEATURE_COLLECTION_TEMPLATE)
    
    for i in range(df.shape[0]):

        # The last row stores the unit of the data
        if i == df.shape[0]-1:
            break
        
        feature = copy.deepcopy(FEATURE_TEMPLATE)
        admin_area_name = list(df.iloc[i])[0]
        # Query the geometry properties of this area
        geo_static_name = '/Users/thomas/Documents/django projects/static/HK_' + str(data.admin_level) + '_polygon.json'
        f = open(geo_static_name, "r")
        boundary = json.load(f)
        
        # Copy boundaries of specified admin level and location
        for district in boundary['features']:
            if 'name' in district['properties'] and district['properties']['name'] == admin_area_name:
                feature['geometry']['type'] = "Polygon"
                feature['geometry']['coordinates'] = district['geometry']['coordinates']

        # Copy the data in the csv file
        feature['properties']['data_for_display'] = list(df.iloc[i])[1:]
        feature['properties']['data_semantics'] = list(df.columns)[1:]
        feature['properties']['admin_area_name'] = list(df.iloc[i])[0]
        feature['properties']['unit'] = list(df.iloc[-1])[1]
        feature['properties']['plotID'] = str(i)

        feature_collection["features"].append(feature)
    
    return render(
        request, "GenericDataView.html", {"data": json.dumps(feature_collection)}
    )
