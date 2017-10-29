# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, redirect,reverse,HttpResponse
from django.contrib import messages
from .models import Buddy, Travel
import bcrypt



def index(request):
    return render(request, 'buddy/index.html')

def register(request):
    results = Buddy.objects.basic_validator(request.POST)
    if type(results) == dict:
        for tag, error in results.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('index'))
    else:
        request.session['id'] = results.id
        request.session['loggedin'] = True
        return redirect(reverse('main'))
    return redirect(reverse('index'))

def login(request):
    results = Buddy.objects.login(request.POST)
    if type(results) == dict:
        for tag, error in results.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('index'))
   
    request.session['id'] = results.id
    request.session['loggedin'] = True
    return redirect(reverse('main'))


def main(request):
    if 'loggedin' not in request.session:
        return redirect(reverse('index'))
    else:
        user = Buddy.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'your_trips': Travel.objects.filter(travelers=user),
            'other_trips': Travel.objects.all().exclude(travelers=user)  
        }
        
        return render(request, 'buddy/main.html', context)

def logout(request):
    request.session.clear()
    return redirect(reverse('index'))

def addtrip(request):
    return render(request, 'buddy/add.html')

def create(request):
    user = Buddy.objects.get(id=request.session['id'])
    results = Travel.objects.create_trip(request.POST,user)
    if type(results) == dict:
        for tag, error in results.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('addtrip'))
    else:
        return redirect(reverse('main'))
    return redirect(reverse('main'))

def join(request, id):
    user = Buddy.objects.get(id=request.session['id'])
    trip = Travel.objects.get(id=id)
    results = Travel.objects.join_trip(user,trip)
    
    return redirect(reverse('main'))

def view(request, id):
    context = {
            'trip': Travel.objects.get(id=id)
        }
    return render(request, 'buddy/trip.html', context)

    



