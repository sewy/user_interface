from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Users ,Travels, Travelslist

# Create your views here.
def index(request):
	return render(request, 'interface/index.html' )

def create_user(request):
	validate = Users.objects.validate(request.POST)
	if validate[0]:
		Users.objects.adduser(request.POST)
		u = Users.objects.get(username=request.POST['username'])
		request.session['user'] = {
					'id': u.id,
					'name': u.name,
					'username': u.username
					}
		return redirect(reverse('showtravel'))
	else:
		Users.objects.errormessage(request, validate[1])
		return redirect(reverse('index'))


def login(request):
	validate = Users.objects.login(request.POST)
	if validate[0]:
		request.session['user'] = {
					'id': validate[1].id,
					'name': validate[1].name,
					'username': validate[1].username
					}
		return redirect(reverse('showtravel'))
	else:
		Users.objects.errormessage(request, validate[1])
		return redirect(reverse('index'))
	return redirect(reverse('showtravel'))

def showtravel(request):
	context = {
		'travels': Travels.objects.filter(user=Users.objects.get(id=request.session['user']['id'])),
		'alltravels': Travels.objects.all(),
		'joinedtravels': Travelslist.objects.filter(user=Users.objects.get(id=request.session['user']['id'])),
		'hides': Travelslist.objects.filter(user=Users.objects.get(id=request.session['user']['id']))
	}
	return render(request,'interface/travels.html', context)

def logout(request):
	request.session.clear()
	return redirect(reverse('index'))

def edittravel(request):
	return render(request,'interface/edittravel.html')

def updatetravel(request):
	validate = Travels.objects.addtravel(request.POST, request.session['user']['id'])
	if validate[0]:
		return redirect(reverse('showtravel'))
	else:
		Users.objects.errormessage(request, validate[1])
		return redirect(reverse('edittravel'))

def jointravel(request, travelid):
	Travelslist.objects.jointravel(request.session['user']['id'], travelid)
	return redirect(reverse('showtravel'))

def showdestination(request, travelid):
	context={
		'travel': Travels.objects.get(id=travelid),
		'users': Travelslist.objects.all()
	}
	return render(request, 'interface/showdestination.html', context)

