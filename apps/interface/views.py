from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def index(request):
		return render(request, 'interface/index.html' )