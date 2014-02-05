from django.shortcuts import render, render_to_response
from django.template.loader import *
import requests

def hello(request):
    return render_to_response('home.html', {})
